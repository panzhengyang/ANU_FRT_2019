import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import sys

if len(sys.argv)<2:
    print('No enough input aurguments')
    print('Example usage is ')
    print('python3 -W ignore station_code')
    sys.exit()

grace_data_file_name = "GRACE_data/GRACE_data_"+sys.argv[1]+".txt"
gps_data_file_name = "GPS_data/GPS_data_"+sys.argv[1]+".txt"

min_data_points = 3

'''
grace_data = np.genfromtxt(grace_data_file_name , 
        delimiter = ' ' ,
        skip_header = 1)
#'''
grace_data = pd.read_csv(grace_data_file_name,
        delimiter=' ',
        header=None,
        skiprows=1,
        dtype=float)
grace_data = np.asarray(grace_data)

print(grace_data.shape)
'''
gps_data = np.genfromtxt(gps_data_file_name ,
        skip_header = 1 ,
        delimiter = None) 
# The data has variable number of spaces seperating columns
# None is the default setting which means any white space is taken as delimiter which include single space, many spaces, tab or many tab etc
#'''
gps_data = pd.read_csv(gps_data_file_name,
        delimiter='\s+',
        header=None,
        skiprows=1)
gps_data = np.asarray(gps_data)
print(gps_data.shape)

# getting the latitude and longitude of the station from station data file 
df=pd.read_csv('station_data.csv',sep='\t')
st=df[df['name'].str.match(sys.argv[1])]
lat = float(st.iloc[0,1])
lon = float(st.iloc[0,2])

# time north north_sigma east east_sigma up up_sigma 
Tgrace , Ngrace , NSgrace , Egrace , ESgrace , Ugrace , USgrace = grace_data[:,0].astype(float) , grace_data[:,1].astype(float) , grace_data[:,2].astype(float) , grace_data[:,3].astype(float), grace_data[:,4].astype(float) , grace_data[:,5].astype(float) , grace_data[:,6].astype(float)

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

Tgps , EIgps , EFgps , NIgps , NFgps , UIgps , UFgps , ESgps , NSgps , USgps = gps_data[:,2].astype(float) , gps_data[:,7].astype(float) , gps_data[:,8].astype(float) , gps_data[:,9].astype(float) , gps_data[:,10].astype(float) , gps_data[:,11].astype(float) , gps_data[:,12].astype(float) , gps_data[:,14].astype(float) , gps_data[:,15].astype(float) , gps_data[:,16].astype(float) 

Egps = EIgps.astype(float) + EFgps.astype(float)
Ngps = NIgps.astype(float) + NFgps.astype(float)
Ugps = UIgps.astype(float) + UFgps.astype(float)

# Converting units m to mm
Egps , Ngps , Ugps = Egps*1000 , Ngps*1000 , Ugps*1000 

# Averaging GPS data at times when GRACE data is available

# DTgrace is the difference of consecutive elements in Tgrace
DTgrace = np.diff(Tgrace)       # length of DTgrace is one less than Tgrace

# Forward Tgrace and Backward Tgrace are the time bounds(upper and lower) of at each Tgrace for taking mean of GPS data at each GRACE data
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

    # Removing mean value from GPS data
    # This process should not be done initially as mean should be calculated based on data when GRACE data is not present
    # This needs further inspection
    ReNgps = ReNgps - ReNgps.mean()
    ReEgps = ReEgps - ReEgps.mean()
    ReUgps = ReUgps - ReUgps.mean()

    # Removing mean value from GRACE data
    # This process is already done for the data but the mean is for all the original data and now not all the initial data is being used
    # This needs further inspection
    ReNgrace = ReNgrace - ReNgrace.mean()
    ReEgrace = ReEgrace - ReEgrace.mean()
    ReUgrace = ReUgrace - ReUgrace.mean()

    # Calculating the RMS values
    rmse_gps = np.sqrt(np.mean((ReUgps.mean()-ReUgps)**2))
    rmse_grace = np.sqrt(np.mean((ReUgrace.mean()-ReUgrace)**2))
    Udiff = ReUgrace - ReUgps
    rms_diff = np.sqrt(np.mean(( Udiff )**2))

    # Calcualting the slope of time series which can be helpful to study Glacial Isostatic Adjustments
    slope_gps = ( ( ReTgps-ReTgps.mean() ).dot( ReUgps-ReUgps.mean() ) )/( ( ReTgps-ReTgps.mean() ).dot( ReTgps-ReTgps.mean() ) )
    slope_grace = ( ( ReTgrace-ReTgrace.mean() ).dot( ReUgrace-ReUgrace.mean() ) )/( ( ReTgrace-ReTgrace.mean() ).dot( ReTgrace-ReTgrace.mean() ) )
    slope_diff = ( ( ReTgps-ReTgps.mean() ).dot( Udiff-Udiff.mean() ) )/( ( ReTgps-ReTgps.mean() ).dot( ReTgps-ReTgps.mean() ) )

    corr_coeff = np.corrcoef(ReUgps,ReUgrace)[1,0]      # corrcoef function gives 2*2 matrix and any element except diagonal ones are equal to corr coef
    
    print('\n\tRMS error of GPS is\t',rmse_gps)
    print('\n\tRMS error of GRACE is\t',rmse_grace)
    print('\n\tRMS of GRACE-GPS is\t',rms_diff)
    print('\n\tSlope of GPS is\t',slope_gps)
    print('\n\tSlope of GRACE is\t',slope_grace)
    print('\n\tSlope of GRACE-GPS is\t',slope_diff)
    print('\n\nCorcoef is \t',corr_coeff)
    

    #'''
    plt.figure("GRACE and Resampled GPS vertical")
    plt.scatter(Tgps,Ugps-Ugps.mean(),label="GPS",s=0.1,c='b')
    plt.plot(Tgrace,Ugrace,label="GRACE",linewidth=3,c='r')
    plt.plot(ReTgps,ReUgps,label="ReGPS",linewidth=3,c='b')
    plt.title("GRACE and ReGPS at "+sys.argv[1])
    plt.xlabel("year")
    plt.ylabel("Vertical (mm)")
    plt.legend()
    plt.show(block=False)
    #'''
    #'''
    plt.figure("Map")
    img = mpimg.imread('images/map.png')
    plt.imshow(img,extent=[-180,180,90,-90])
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
