import numpy as np
import matplotlib.pyplot as plt

grace_data_file_name = "ts_-25.037_128.296_50_edefn_1558487733.csv"
gps_data_file_name = "WARA.IGS08.tenv3.txt"

grace_data = np.genfromtxt(grace_data_file_name , 
        delimiter = ' ' ,
        skip_header = 1)

print(grace_data.shape)

gps_data = np.genfromtxt(gps_data_file_name ,
        skip_header = 1 ,
        delimiter = None) 
# The data has variable number of spaces seperating columns
# None is the default setting which means any white space is taken as delimiter which include single space, many spaces, tab or many tab etc

print(gps_data.shape)

# time north north_sigma east east_sigma up up_sigma 
Tgrace , Ngrace , NSgrace , Egrace , ESgrace , Ugrace , USgrace = grace_data[:,0].astype(float) , grace_data[:,1].astype(float) , grace_data[:,2].astype(float) , grace_data[:,3].astype(float), grace_data[:,4].astype(float) , grace_data[:,5].astype(float) , grace_data[:,6].astype(float)

""" Example line for gps:

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
"""

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
BTgrace = Tgrace - np.pad(DTgrace,(1,0),'constnat',constant_values = (0,0)) / 2



"""
plt.figure("GPS and GRACE vertical")
plt.plot(Tgrace,Ugrace,label="GRACE")
plt.plot(Tgps,Ugps-Ugps.mean(),'.',label="GPS")
plt.title("GRACE and GPS at WARA")
plt.xlabel("year")
plt.ylabel("Vertical (mm)")
plt.legend()
#"""
"""
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
#"""
plt.show()

