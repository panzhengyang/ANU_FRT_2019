# The results of this code will be slightly different from compare.py. This is because the FTgrace, BTgrace in compare.py are calculated after the Tgrace is filtered for the Tmin, Tmax range. 
# In this file FTgrace and BTgrace are calculated befre filtering Tgrace and filtering is done later while calculations of rms and slope. This is done so that the data is not lost (by initial filtering) and can be shown in the plots even though it is not considered for calculation.
# The difference arrises when calculating DTgrace, when filtered in the first, the last FTgrace and first BTgrace elements are based on the padded 0 of DTgrace. When the filtering is not done, the corresponding element of FTgrace and BTgrace do not use the padded 0, rather use the actual next/previous time stamp in Tgrace. 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pandas import read_csv
from numpy import cos,sin,sqrt
import sys
from scipy.special import lpmv
from scipy.special import factorial as fact

Tmax = 2011.33333333
Tmin = 2001.0

if len(sys.argv)<3:
    print('No enough input aurguments')
    print('Example usage is ')
    print('python3 -W ignore this_file_name station_code GPS_dataset_code')
    sys.exit()

grace_data_file_name = "GRACE_data/GRACE_data_"+sys.argv[1]+".txt"

min_data_points = 3

grace_data = read_csv(grace_data_file_name,
        delimiter=' ',
        header=None,
        skiprows=0,
        dtype=float)
grace_data = np.asarray(grace_data)

# time north north_sigma east east_sigma up up_sigma 
Tgrace , Ugrace , USgrace = grace_data[:,0].astype(float) , grace_data[:,5].astype(float) , grace_data[:,6].astype(float)


if sys.argv[2] == 'N' :
    #''' For NGL         
    gps_data_file_name = "NGL_GPS_data/GPS_data_"+sys.argv[1]+".txt"
    gps_data = read_csv(gps_data_file_name,
            delimiter='\s+',
            header=None,
            skiprows=1)
    gps_data = np.asarray(gps_data)
    #print(gps_data.shape)

    Tgps ,  UIgps , UFgps , USgps = gps_data[:,2].astype(float)  , gps_data[:,11].astype(float) , gps_data[:,12].astype(float)  , gps_data[:,16].astype(float) 

    Ugps = UIgps.astype(float) + UFgps.astype(float)

    # Converting units m to mm
    Ugps =  Ugps*1000 
    #'''

elif sys.argv[2] == 'M' :

    #''' For MIT        
    gps_data_file_name = "MIT_GPS_data/GPS_data_"+sys.argv[1]+".txt"
    gps_data = read_csv(gps_data_file_name,
            delimiter='\s+',
            header=None,
            skiprows=0)
    gps_data = np.asarray(gps_data)
    #print(gps_data.shape)

    Tgps ,  Ugps , USgps = gps_data[:,0].astype(float) , gps_data[:,19].astype(float) , gps_data[:,25].astype(float)  

    # Converting units mm
    Ugps = Ugps*1000 
    #'''

# getting the latitude and longitude of the station from station data file 
df=read_csv('station_data.txt',sep='\s+')
st=df[df['name'].str.match(sys.argv[1])]
lat = float(st.iloc[0,1])
lon = float(st.iloc[0,2])
if lon > 180:
    lon = lon-360.0
print(lat,lon)
colat = ( 90-lat )*np.pi/180
lat = lat*np.pi/180
lon = lon*np.pi/180

coeff_file_name = sys.argv[3]

############## Reading Load Love numbers
# This is not done in usual way since the symbol for exponent in Load_Love2_CM.dat file is 'D' rather than 'E'. 'D' cannot be interpretted as exponent in python so the character D is replaced with E for all the columns with data as string. Once replaced, it is converted to float.
load_love_file_name = 'Load_Love2_CM.dat'
load_love_pd_dataframe =  read_csv(load_love_file_name, header = None, skiprows = 13, sep = '\s+',
        dtype = str)
load_love_pd_dataframe[1] = load_love_pd_dataframe[1].str.replace('D','E')
load_love_pd_dataframe[2] = load_love_pd_dataframe[2].str.replace('D','E')
load_love_pd_dataframe[3] = load_love_pd_dataframe[3].str.replace('D','E')
load_love_data = np.asarray(load_love_pd_dataframe,
        dtype = float)
h = load_love_data[:,1]
k = load_love_data[:,3]


############## Function values for visco-elastic and vertical elastic
radius_of_earth = 6378100.0     # in meters m
Fv = radius_of_earth*(1.1677 * load_love_data[:,0]  - 0.5233)     # Fv values depends on the degree, first column of load_love_data is degree
Fe =  radius_of_earth * h/(1+k) # This has inf and nan
Fe[0] = 0   # in CM frame degree 0 and 1 cannot be calculated  
Fe[1] = 0


############## Normalised Associated Legendre function
# refer :   http://mitgcm.org/~mlosch/geoidcookbook/node11.html
#           https://igortitara.files.wordpress.com/2010/04/handbook-of-math-for-engineers-and-scientists1.pdf
def nalf(n,m,x):
    # order degree input
    return lpmv(m,n,x) * (-1)**m * sqrt( (2-float(m==0)) * (2.0*n + 1) * fact(n-m)/fact(n+m) )


data = np.asarray( read_csv( coeff_file_name , header = None , skiprows = 0 , sep = '\s+' ) ) 
n = data[:,0].astype(int)
m = data[:,1].astype(int)
C = data[:,2].astype(float)
S = data[:,3].astype(float)

elastic_correction_rate = 0.0
only_visco_elastic_rate = 0.0
geoid = 0.0
visco_correction_rate = 0.0
for i in range( np.size(n)): 
    elastic_correction_rate         += nalf( n[i] , m[i] , cos(colat) ) * Fe[n[i]] * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    only_visco_elastic_rate   += nalf( n[i] , m[i] , cos(colat) ) * Fv[n[i]] * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    geoid           += nalf( n[i] , m[i] , cos(colat) ) * radius_of_earth * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    visco_correction_rate  += nalf( n[i] , m[i] , cos(colat) ) * ( Fv[n[i]] - Fe[n[i]] )* ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 




# DTgrace is the difference of consecutive elements in Tgrace
DTgrace = np.diff(Tgrace)       # length of DTgrace is one less than ReTgrace

# Forward ReTgrace and Backward ReTgrace are the time bounds(upper and lower) of at each ReTgrace for taking mean of GPS data at each GRACE data
# DTgrace is padded since it is one element less than Tgrace
FTgrace = Tgrace + np.pad(DTgrace,(0,1),'constant',constant_values = (0,0)) / 2          
BTgrace = Tgrace - np.pad(DTgrace,(1,0),'constant',constant_values = (0,0)) / 2


# I don't know how to avoid this loop


ReTgps = Tgrace
ReUgps = Ugrace * 0
ReUSgps = USgrace * 0
data_flag = (Tgrace * 0).astype(bool)

for i in range(np.size(Tgrace)):
    selection_flag = np.logical_and( Tgps <= FTgrace[i] , Tgps > BTgrace[i] ) 
    data_flag[i] = selection_flag.sum()     # gets boolean elements, not integers 
    ReUgps[i] = Ugps[ selection_flag ].mean()
    ReUSgps[i] = USgps[ selection_flag ].mean()


if data_flag.sum() > min_data_points :
    # selecting data only when both GRACE and GPS are simultaniously available
    ReTgps = ReTgps[data_flag]
    ReUgps = ReUgps[data_flag]
    ReUSgps = ReUSgps[data_flag]

    ReTgrace = Tgrace[data_flag]
    ReUgrace = Ugrace[data_flag]
    ReUSgrace = USgrace[data_flag]
    
    # time_range_flag, trf is to select only the samples within the range of (Tmin,Tmax)
    trf = np.logical_and(ReTgrace > Tmin , ReTgrace < Tmax)
    
    # Storing the mean value of Ugps as this value is required later during plotting and cannot be acquired after the later steps
    Ugps_mean = ReUgps[trf].mean()
    
    # Removing mean value from GPS data
    # This process should not be done initially as mean should be calculated based on data when GRACE data is not present
    # This needs further inspection
    ReUgps = ReUgps - ReUgps[trf].mean()

    only_elastic_grace = ReUgrace - 1000*elastic_correction_rate*ReTgrace
    only_visco_elastic_grace = 1000*only_visco_elastic_rate*ReTgrace
    
    corrected_grace = ReUgrace + 1000*visco_correction_rate*ReTgrace

    # Removing mean value from GRACE data
    # This process is already done for the data but the mean is for all the original data and now not all the initial data is being used
    # This needs further inspection
    ReUgrace = ReUgrace - ReUgrace[trf].mean()
    only_elastic_grace = only_elastic_grace - only_elastic_grace[trf].mean()
    only_visco_elastic_grace = only_visco_elastic_grace - only_visco_elastic_grace[trf].mean()
    corrected_grace = corrected_grace - corrected_grace[trf].mean()

    # Calculating the RMS values
    rmse_gps = np.sqrt(np.mean((ReUgps[trf].mean()-ReUgps[trf])**2))
    rmse_grace = np.sqrt(np.mean((ReUgrace[trf].mean()-ReUgrace[trf])**2))
    Udiff = ReUgrace - ReUgps
    rms_diff = np.sqrt(np.mean(( Udiff[trf] )**2))

    # Calcualting the slope of time series which can be helpful to study Glacial Isostatic Adjustments
    slope_gps = ( ( ReTgps[trf]-ReTgps[trf].mean() ).dot( ReUgps[trf]-ReUgps[trf].mean() ) )/( ( ReTgps[trf]-ReTgps[trf].mean() ).dot( ReTgps[trf]-ReTgps[trf].mean() ) )
    slope_grace = ( ( ReTgrace[trf]-ReTgrace[trf].mean() ).dot( ReUgrace[trf]-ReUgrace[trf].mean() ) )/( ( ReTgrace[trf]-ReTgrace[trf].mean() ).dot( ReTgrace[trf]-ReTgrace[trf].mean() ) )
    slope_diff = ( ( ReTgps[trf]-ReTgps[trf].mean() ).dot( Udiff[trf]-Udiff[trf].mean() ) )/( ( ReTgps[trf]-ReTgps[trf].mean() ).dot( ReTgps[trf]-ReTgps[trf].mean() ) )

    corr_coeff = np.corrcoef(ReUgps[trf],ReUgrace[trf])[1,0]      # corrcoef function gives 2*2 matrix and any element except diagonal ones are equal to corr coef
    
    print('No of data points:\t',trf.sum())
    print('RMS error of GPS is\t',rmse_gps)
    print('RMS error of GRACE is\t',rmse_grace)
    print('RMS of GRACE-GPS is\t',rms_diff)
    print('Slope of GPS is\t\t',slope_gps)
    print('Slope of GRACE is\t',slope_grace)
    print('Slope of GRACE-GPS is\t',slope_diff)
    print('Corcoef is \t',corr_coeff)
    print('Only visco-elastic slope: \t',only_visco_elastic_rate*1000)
    print('Only elastic slope: \t',slope_grace-elastic_correction_rate*1000)
    print('corrected GRACE slope: \t',slope_grace-visco_correction_rate*1000)

    #'''
    plt.figure("GRACE and Resampled GPS vertical")
    plt.scatter(Tgps,Ugps-Ugps_mean,label="GPS",s=0.05,c='b')
    plt.plot(ReTgrace,ReUgrace,label="GRACE",linewidth=2,c='r')
    plt.plot(ReTgps,ReUgps,label="ReGPS",linewidth=2,c='b')
    plt.plot(ReTgrace,only_elastic_grace,label="elastic_GRACE",linewidth=2,c='y')
    plt.plot(ReTgrace,only_visco_elastic_grace,label="visco_elastic_GRACE",linewidth=2,c='g')
    plt.plot(ReTgrace,corrected_grace,label="corrected_GRACE",linewidth=2,c='k')
    plt.title("GRACE and ReGPS at "+sys.argv[1])
    plt.xlabel("year")
    plt.ylabel("Vertical (mm)")
    plt.legend()
    plt.show(block=False)
    #'''
    #'''
    plt.figure("Map")
    img = mpimg.imread('../images/map.png')
    plt.imshow(img,extent=[-180,180,-90,90])
    plt.scatter(lon*180/np.pi,lat*180/np.pi)
    plt.title('Location of station '+sys.argv[1])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show(block=False)
    #'''
    '''
    plt.figure("Selected GRACE and GPS data")
    plt.plot(ReTgps,ReUgps,label="GPS")
    plt.plot(ReTgrace,ReUgrace,label="GRACE")
    plt.xlabel("year")
    plt.ylabel("Vertical (mm)")
    plt.title("Selected data of GRACE and GPS")
    plt.legend()
    #'''
    '''
    plt.figure("GPS and GRACE vertical")
    plt.plot(Tgrace,Ugrace,label="GRACE")
    plt.plot(Tgps,Ugps,'.',label="GPS")
    plt.title("GRACE and GPS at WARA")
    plt.xlabel("year")
    plt.ylabel("Vertical (mm)")
    plt.legend()
    #'''
    '''
    plt.figure("GPS and GRACE all data")
    plt.subplot(231)
    plt.plot(Tgps,Egps)
    plt.title("GPS East")
    plt.subplot(232)
    plt.plot(Tgps,Ngps)
    plt.title("GPS North")
    plt.subplot(233)
    plt.plot(Tgps,Ugps)
    plt.title("GPS Up")
    plt.subplot(234)
    plt.plot(Tgrace,Egrace)
    plt.title("GRACE East")
    plt.subplot(235)
    plt.plot(Tgrace,Ngrace)
    plt.title("GRACE North")
    plt.subplot(236)
    plt.plot(Tgrace,Ugrace)
    plt.title("GRACE Up")
    #'''
    plt.show()

else : 
    print('no sufficient data available')
