from scipy.special import lpmv
from scipy.special import factorial as fact 
from numpy import sqrt
from numpy import cos
from numpy import sin
import numpy as np 
import pandas as pd 
from sys import argv

coeff_rate_file_name = argv[1] #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
lat = float(argv[3]) #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
lon = float(argv[4]) #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
out_file_name = argv[2] #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
colat = ( 90-lat ) * np.pi/180.0        # colatitude in radians
lon = ( lon - 360.0*float(lon > 180) ) * np.pi/180.0    # lon is in radians from here
max_degree = 80 


############## Reading Load Love numbers
# This is not done in usual way since the symbol for exponent in Load_Love2_CM.dat file is 'D' rather than 'E'. 'D' cannot be interpretted as exponent in python so the character D is replaced with E for all the columns with data as string. Once replaced, it is converted to float.
load_love_file_name = 'Load_Love2_CM.dat'
load_love_pd_dataframe =  pd.read_csv(load_love_file_name, header = None, skiprows = 13, sep = '\s+',
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
Fv = radius_of_earth*( 1.1677 * load_love_data[:,0]  + 0.5233)     # Fv values depends on the degree, first column of load_love_data is degree
Fe =  radius_of_earth * h/(1+k) # This has inf and nan
Fe[0] = 0   # in CM frame degree 0 and 1 cannot be calculated  
Fe[1] = 0


############## Reading coeff rate file
coeff_rate = np.asarray ( pd.read_csv( coeff_rate_file_name , header = None , skiprows = 0 , sep = '\s+'  ) , dtype = float )
# column info : degree order C S sigma_C sigma_S

############## functions to get the coefficient corresponding to degree n and order m easily. This changes if the coefficient file changes. 
def C(n,m):
    return coeff_rate[ (n*(n+1)/2) + m -1 , 2]

def S(n,m):
    return coeff_rate[ (n*(n+1)/2) + m -1 , 3]


############## Normalised Associated Legendre function
# refer :   http://mitgcm.org/~mlosch/geoidcookbook/node11.html
#           https://igortitara.files.wordpress.com/2010/04/handbook-of-math-for-engineers-and-scientists1.pdf
# Not clear enough how -1^m 
def nalf(n,m,x):
    # order degree input
    return lpmv(m,n,x) * (-1)**m * sqrt( (2-float(m==0)) * (2.0*n + 1) * fact(n-m)/fact(n+m) )


############## calculation
out = np.zeros( ( ( ( ((max_degree+1)*max_degree/2) + 1 + max_degree )*2 - 3*2  + 1) , 3 ))
#                 <  combinations of all deg & order with 0 deg  >*2 for coeff of sin and cos, -3 for not including deg 0&1 *2 for two coeff, +1 for Edot and total 3 columns for saving deg order values as well
Edot = 0.0
count = 0
#for n in np.linspace(2 ,3 ,2 , dtype = int ) :
for n in np.linspace(2 , max_degree , max_degree -1 , dtype = int ) :   # not for degree 0 and 1 
    for m in range(n + 1):
        Edot += nalf(n,m,cos(colat)) * Fe[n] * ( C(n,m)*cos(m*lon) + S(n,m)*sin(m*lon) )
        out[ (m+n*(n+1)/2)*2 - 5 , 2 ]   = nalf(n,m,cos(colat)) * (Fv[n] - Fe[n]) * cos(m*lon)
        out[ (m+n*(n+1)/2)*2 - 4 , 2 ]   = nalf(n,m,cos(colat)) * (Fv[n] - Fe[n]) * sin(m*lon)
        out[ (m+n*(n+1)/2)*2 - 5 , 0 ]   = n
        out[ (m+n*(n+1)/2)*2 - 4 , 0 ]   = n
        out[ (m+n*(n+1)/2)*2 - 5 , 1 ]   = m
        out[ (m+n*(n+1)/2)*2 - 4 , 1 ]   = m

out[0,0] = -1
out[0,1] = -1 
out[0,2] = Edot
out[:,2] = out[:,2] * 1000    # converting to mm millimeter

# format in multipling factors of : 1 C20 S20 C21 S21 C22 S22 C30 S30 C31 S31 .... 
np.savetxt(out_file_name,out,fmt='%d %d %.18e')
