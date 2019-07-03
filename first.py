# The results of this code will be slightly different from compare.py. This is because the FTgrace, BTgrace in compare.py are calculated after the Tgrace is filtered for the Tmin, Tmax range. 
# In this file FTgrace and BTgrace are calculated befre filtering Tgrace and filtering is done later while calculations of rms and slope. This is done so that the data is not lost (by initial filtering) and can be shown in the plots even though it is not considered for calculation.
# The difference arrises when calculating DTgrace, when filtered in the first, the last FTgrace and first BTgrace elements are based on the padded 0 of DTgrace. When the filtering is not done, the corresponding element of FTgrace and BTgrace do not use the padded 0, rather use the actual next/previous time stamp in Tgrace. 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import sys

Tmax = 2011.33333333
Tmin = 2001.0

if len(sys.argv)<3:
    print('No enough input aurguments')
    print('Example usage is ')
    print('python3 -W ignore this_file_name station_code GPS_dataset_code')
    sys.exit()

grace_data_file_name = "GRACE_data/GRACE_data_"+sys.argv[1]+".txt"

min_data_points = 3

if len(sys.argv) > 3 :
    grace_data_file_name = sys.argv[3]
    # header needs to be removed from this file

grace_data = pd.read_csv(grace_data_file_name,
        delimiter=' ',
        header=None,
        skiprows=0,
        dtype=float)
grace_data = np.asarray(grace_data)

# time north north_sigma east east_sigma up up_sigma 
Tgrace , Ngrace , NSgrace , Egrace , ESgrace , Ugrace , USgrace = grace_data[:,0].astype(float) , grace_data[:,1].astype(float) , grace_data[:,2].astype(float) , grace_data[:,3].astype(float), grace_data[:,4].astype(float) , grace_data[:,5].astype(float) , grace_data[:,6].astype(float)

#print(grace_data.shape)
'''
gps_data = np.genfromtxt(gps_data_file_name ,
        skip_header = 1 ,
        delimiter = None) 
# The data has variable number of spaces seperating columns
# None is the default setting which means any white space is taken as delimiter which include single space, many spaces, tab or many tab etc
#'''

if sys.argv[2] == 'N' :
    #''' For NGL         
    gps_data_file_name = "NGL_GPS_data/GPS_data_"+sys.argv[1]+".txt"
    gps_data = pd.read_csv(gps_data_file_name,
            delimiter='\s+',
            header=None,
            skiprows=1)
    gps_data = np.asarray(gps_data)
    #print(gps_data.shape)

    Tgps , EIgps , EFgps , NIgps , NFgps , UIgps , UFgps , ESgps , NSgps , USgps = gps_data[:,2].astype(float) , gps_data[:,7].astype(float) , gps_data[:,8].astype(float) , gps_data[:,9].astype(float) , gps_data[:,10].astype(float) , gps_data[:,11].astype(float) , gps_data[:,12].astype(float) , gps_data[:,14].astype(float) , gps_data[:,15].astype(float) , gps_data[:,16].astype(float) 

    Egps = EIgps.astype(float) + EFgps.astype(float)
    Ngps = NIgps.astype(float) + NFgps.astype(float)
    Ugps = UIgps.astype(float) + UFgps.astype(float)

    # Converting units m to mm
    Egps , Ngps , Ugps = Egps*1000 , Ngps*1000 , Ugps*1000 
    #'''

elif sys.argv[2] == 'M' :

    #''' For MIT        
    gps_data_file_name = "MIT_GPS_data/GPS_data_"+sys.argv[1]+".txt"
    gps_data = pd.read_csv(gps_data_file_name,
            delimiter='\s+',
            header=None,
            skiprows=0)
    gps_data = np.asarray(gps_data)
    #print(gps_data.shape)

    Tgps , Elon , Nlat , Ugps , ESgps , NSgps , USgps = gps_data[:,0].astype(float) , gps_data[:,18].astype(float) , gps_data[:,17].astype(float) , gps_data[:,19].astype(float) , gps_data[:,24].astype(float) , gps_data[:,23].astype(float) , gps_data[:,25].astype(float)  

    Earth_radius = 6.3781*10**6     # meters
    # Converting units mm
    Egps , Ngps , Ugps = Earth_radius*np.sin(Nlat*np.pi/180)*(Elon-Elon[0])*1000 , Earth_radius*((Nlat-Nlat[0])*np.pi/180.)*1000 , Ugps*1000 
    #'''

# getting the latitude and longitude of the station from station data file 
df=pd.read_csv('station_data.csv',sep='\s+')
st=df[df['name'].str.match(sys.argv[1])]
lat = float(st.iloc[0,1])
lon = float(st.iloc[0,2])
if lon > 180:
    lon = lon-360.0
print(lat,lon)


'''
# Selecting the GRACE data which is only in a particular time intervel 
grace_select_flag = np.logical_and((Tgrace > Tmin),(Tgrace < Tmax))

Tgrace = Tgrace[grace_select_flag]
Ngrace = Ngrace[grace_select_flag]
NSgrace = NSgrace[grace_select_flag]
Egrace = Egrace[grace_select_flag]
ESgrace = ESgrace[grace_select_flag]
Ugrace = Ugrace[grace_select_flag]
USgrace = USgrace[grace_select_flag]
#'''

''' Example line for gps:

-------------------
COVE 10JUL28 2010.5708 55405 1594 4 -112.8  -3815 -0.41548   4276712 0.86481  1687  0.35637  0.1800 0.00065 0.00067 0.00328  0.05829 -0.56488  0.04405
-------------------

Meaning of columns:

1.  COVE      station name
2.  10JUL28   date
3.  2010.5708 decimal year
4.  55405     modified Julian day
5.  1594      GPS week
6.  4         day of GPS week
7.  -112.8    longitude (degrees) of reference meridian
8.  -3815     eastings (m), integer portion (from ref. meridian)
9.  -0.41548  eastings (m), fractional portion
10.  4276712  northings (m), integer portion (from equator)
11.  0.86481  northings (m), fractional portion
12.  1687     vertical (m), integer portion
13.  0.35637  vertical (m), fractional portion
14. 0.1800    antenna height (m) assumed from Rinex header
15. 0.00065   east sigma (m)
16. 0.00067   north sigma (m)
17. 0.00328   vertical sigma (m)
18.  0.05829  east-north correlation coefficient
19. -0.56488  east-vertical correlation coefficient
20.  0.04405  north-vertical correlation coefficient
'''



# DTgrace is the difference of consecutive elements in Tgrace
DTgrace = np.diff(Tgrace)       # length of DTgrace is one less than ReTgrace

# Forward ReTgrace and Backward ReTgrace are the time bounds(upper and lower) of at each ReTgrace for taking mean of GPS data at each GRACE data
# DTgrace is padded since it is one element less than Tgrace
FTgrace = Tgrace + np.pad(DTgrace,(0,1),'constant',constant_values = (0,0)) / 2          
BTgrace = Tgrace - np.pad(DTgrace,(1,0),'constant',constant_values = (0,0)) / 2


# I don't know how to avoid this loop


ReTgps = Tgrace
ReNgps = Ngrace * 0
ReEgps = Egrace * 0
ReUgps = Ugrace * 0
ReNSgps = NSgrace * 0
ReESgps = ESgrace * 0
ReUSgps = USgrace * 0
data_flag = (Tgrace * 0).astype(bool)

for i in range(np.size(Tgrace)):
    
    selection_flag = np.logical_and( Tgps <= FTgrace[i] , Tgps > BTgrace[i] ) 
    data_flag[i] = selection_flag.sum()     # gets boolean elements, not integers 
    
    #print(selection_flag.sum())
    #print(data_flag[i])

    ReNgps[i] = Ngps[ selection_flag ].mean()
    ReEgps[i] = Egps[ selection_flag ].mean()
    ReUgps[i] = Ugps[ selection_flag ].mean()
    
    ReNSgps[i] = NSgps[ selection_flag ].mean()
    ReESgps[i] = ESgps[ selection_flag ].mean()
    ReUSgps[i] = USgps[ selection_flag ].mean()


if data_flag.sum() > min_data_points :
    # selecting data only when both GRACE and GPS are simultaniously available
    ReTgps = ReTgps[data_flag]
    ReNgps = ReNgps[data_flag]
    ReEgps = ReEgps[data_flag]
    ReUgps = ReUgps[data_flag]
    ReNSgps = ReNSgps[data_flag]
    ReESgps = ReESgps[data_flag]
    ReUSgps = ReUSgps[data_flag]

    ReTgrace = Tgrace[data_flag]
    ReNgrace = Ngrace[data_flag]
    ReEgrace = Egrace[data_flag]
    ReUgrace = Ugrace[data_flag]
    ReNSgrace = NSgrace[data_flag]
    ReESgrace = ESgrace[data_flag]
    ReUSgrace = USgrace[data_flag]
    
    
    # time_range_flag, trf is to select only the samples within the range of (Tmin,Tmax)
    trf = np.logical_and(ReTgrace > Tmin , ReTgrace < Tmax)
    
    # Storing the mean value of Ugps as this value is required later during plotting and cannot be acquired after the later steps
    Ugps_mean = ReUgps[trf].mean()
    
    # Removing mean value from GPS data
    # This process should not be done initially as mean should be calculated based on data when GRACE data is not present
    # This needs further inspection
    ReNgps = ReNgps - ReNgps[trf].mean()
    ReEgps = ReEgps - ReEgps[trf].mean()
    ReUgps = ReUgps - ReUgps[trf].mean()

    # Removing mean value from GRACE data
    # This process is already done for the data but the mean is for all the original data and now not all the initial data is being used
    # This needs further inspection
    ReNgrace = ReNgrace - ReNgrace[trf].mean()
    ReEgrace = ReEgrace - ReEgrace[trf].mean()
    ReUgrace = ReUgrace - ReUgrace[trf].mean()

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
    

    #'''
    plt.figure("GRACE and Resampled GPS vertical")
    plt.scatter(Tgps,Ugps-Ugps_mean,label="GPS",s=0.05,c='b')
    plt.plot(ReTgrace,ReUgrace,label="GRACE",linewidth=2,c='r')
    plt.plot(ReTgps,ReUgps,label="ReGPS",linewidth=2,c='b')
    plt.title("GRACE and ReGPS at "+sys.argv[1])
    plt.xlabel("year")
    plt.ylabel("Vertical (mm)")
    plt.legend()
    plt.show(block=False)
    #'''
    #'''
    plt.figure("Map")
    img = mpimg.imread('images/map.png')
    plt.imshow(img,extent=[-180,180,-90,90])
    plt.scatter(lon,lat)
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
