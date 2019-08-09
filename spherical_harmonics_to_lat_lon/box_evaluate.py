from scipy.special import lpmv
from scipy.special import factorial as fact
from numpy import sqrt
from numpy import cos
from numpy import sin 
import numpy as np 
from pandas import read_csv
from sys import argv 
import matplotlib.pyplot as plt 
from PIL import Image

coeff_file_name = argv[1]

min_lat = float(argv[2])
max_lat = float(argv[3])
min_lon = float(argv[4])
max_lon = float(argv[5])

lon_resolution = int(argv[6])
lat_resolution = int( lon_resolution*abs((max_lat - min_lat)/(max_lon - min_lon)))

lat_array = np.linspace(max_lat,min_lat,lat_resolution)
lon_array = np.linspace(min_lon,max_lon,lon_resolution)

lon , lat = np.meshgrid(lon_array,lat_array)

abs_range = 15
#print(lon)
#print(lat)


colat = ( 90 - lat )*np.pi/180.0 
lon = ( lon - 360.0*(lon > 180.0).astype(float) )*np.pi/180.0 


############## station_list
station_list_file = argv[7]
station_pd_dataframe = read_csv(station_list_file, header = None , sep = '\s+')
station_list = np.asarray(station_pd_dataframe)
lat_list = station_list[:,1]
lon_list = station_list[:,2]


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

elastic = 0.0
visco_elastic = 0.0
geoid = 0.0
least_square_compute = 0.0
for i in range( np.size(n)): 
    elastic         += nalf( n[i] , m[i] , cos(colat) ) * Fe[n[i]] * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    #visco_elastic   += nalf( n[i] , m[i] , cos(colat) ) * Fv[n[i]] * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    visco_elastic   += nalf( n[i] , m[i] , cos(colat) ) * radius_of_earth*(1.1677*n[i] - 0.5233) * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    #visco_elastic   += nalf( n[i] , m[i] , cos(colat) ) * radius_of_earth*(2.0*n[i] + 1.0) * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    geoid           += nalf( n[i] , m[i] , cos(colat) ) * radius_of_earth * ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    least_square_compute  += nalf( n[i] , m[i] , cos(colat) ) * ( Fv[n[i]] - Fe[n[i]] )* ( C[i]*cos(m[i]*lon) + S[i]*sin(m[i]*lon) ) 
    print(n[i],m[i])

#print('elastic :\t' ,elastic*1000 )
#print( 'visco elastic :\t', visco_elastic*1000 )
#print( 'geoid  :\t', geoid*1000 )
#print(least_square_compute)

#'''
mask = np.logical_or((visco_elastic*1000 > abs_range ),(visco_elastic*1000 < -abs_range ))
visco_elastic = np.ma.masked_where(mask,visco_elastic)
#'''


plt.figure(0)

pil_img = Image.open('../images/map.png')
pil_img.load()
map_data = np.asarray(pil_img)[:,:,0]

coast = map_data

#'''
map_mask = coast > 200
coast = 255*(coast>200).astype(float)
coast = np.ma.masked_where(map_mask,coast)
#'''

plt.imshow(visco_elastic*1000,extent=[min_lon,max_lon,min_lat,max_lat],alpha = 1,cmap='bwr')
plt.colorbar()
plt.imshow(coast*1000,extent=[-180,180,-90,90],alpha = 1,cmap='gray')
plt.scatter(lon_list,lat_list,s=60,c='c')
plt.imshow(visco_elastic*1000,extent=[min_lon,max_lon,min_lat,max_lat],alpha = 0)

plt.show()
