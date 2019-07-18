from scipy.special import lpmv
from scipy.special import factorial as fact
from numpy import sqrt
from numpy import cos
from numpy import sin 
import numpy as np 
from pandas import read_csv
from sys import argv 


coeff_file_name = './visco_coeff_mit_above_50.txt'
coeff_file_name = argv[1]
lat = float(argv[2] )
lon = float(argv[3] )
#lat = float(66.987) 
#lon = float(-50.945) 
colat = ( 90 - lat )*np.pi/180.0 
lon = ( lon - 360.0*float(lon > 180.0) )*np.pi/180.0 


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

print('elastic :\t' ,elastic*1000 )
print( 'visco elastic :\t', visco_elastic*1000 )
#print( 'geoid  :\t', geoid*1000 )
print(least_square_compute)
