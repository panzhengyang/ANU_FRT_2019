# This code is to calculate the slopes of coefficients and position time series

import numpy as np
import pandas as pd 
import sys
from scipy.stats import linregress

Tmax = 2011.33333333
Tmin = 2001.0


grace_time_stamps_file = '../GRACE_data/time_decimal_years.txt'

Tgrace_pd_dataframe = pd.read_csv(grace_time_stamps_file,
        header=None,
        skiprows=0,
        dtype=float)
Tgrace = np.asarray( Tgrace_pd_dataframe , dtype = float)

grace_names_file = '../GRACE_data/names.txt'
grace_names_pd_dataframe = pd.read_csv(grace_names_file ,
        header = None, 
        skiprows = 0,
        dtype = str)
grace_names = np.asarray(grace_names_pd_dataframe , dtype = str)

station_name = str(sys.argv[1])
latitude = float(sys.argv[2])
longitude = float(sys.argv[3])
#station_name = 'HYDE'
#latitude = 17.417259 
#longitude = 78.550870

longitue = longitude - 360.0*bool(longitude>180)

if( sys.argv[4] == 'mit' or sys.argv[4] == 'MIT' ):
    ############## For MIT 
    gps_data_file = '../MIT_GPS_data/GPS_data_'+station_name+'.txt'
    gps_data_pd_dataframe = pd.read_csv(gps_data_file , 
            delimiter = '\s+',
            header = None,
            skiprows = 0)
    gps_data = np.asarray(gps_data_pd_dataframe )

    Tgps , Ugps , USgps = gps_data[:,0].astype(float) , gps_data[:,19].astype(float) , gps_data[:,25].astype(float)
    Ugps = Ugps #* 1000      # converting to mm millimeter

elif( sys.argv[4] == 'ngl' or sys.argv[4] == 'NGL' ):
    ############## For NGL 
    gps_data_file = '../NGL_GPS_data/GPS_data_'+station_name+'.txt'
    gps_data_pd_dataframe = pd.read_csv(gps_data_file , 
            delimiter = '\s+',
            header = None,
            skiprows = 1)
    gps_data = np.asarray(gps_data_pd_dataframe )

    Tgps , UIgps , UFgps , USgps = gps_data[:,2].astype(float) , gps_data[:,11].astype(float) , gps_data[:,12].astype(float) , gps_data[:,16].astype(float)
    Ugps = (UIgps+UFgps) #* 1000      # converting to mm millimeter


############## GRACE time window
grace_selection_flag = np.logical_and( Tgrace > Tmin , Tgrace < Tmax ) 
Tgrace = Tgrace[ grace_selection_flag ]
grace_names = grace_names[grace_selection_flag]

# refer first.py file
DTgrace = np.diff(Tgrace)
FTgrace = Tgrace + np.pad(DTgrace,(0,1),'constant',constant_values = (0,0)) / 2
BTgrace = Tgrace - np.pad(DTgrace,(1,0),'constant',constant_values = (0,0)) / 2

ReTgps = Tgrace 
ReUgps = Tgrace * 0 
ReUSgps = Tgrace * 0 
data_flag = (Tgrace * 0).astype(bool)

for i in range(np.size(Tgrace)):
    selection_flag = np.logical_and( Tgps <= FTgrace[i] , Tgps > BTgrace[i] )
    data_flag[i] = selection_flag.sum() 

    ReUgps[i] = Ugps[ selection_flag ].mean()
    ReUSgps[i] = USgps[ selection_flag ].mean()


############## GPS calculation
ReTgps = ReTgps[data_flag]
ReUgps = ReUgps[data_flag]
ReUSgps = ReUSgps[data_flag]

gps_slope , gps_intercept , gps_r , gps_p , gps_std = linregress(ReTgps, ReUgps)

############## GRACE calculation
re_grace_names = grace_names[data_flag]
ReTgrace = Tgrace[data_flag]

no_files = np.size(re_grace_names)

coeff_file_name_prefix = '../GRACE_data/'

coeff_file_rows , coeff_file_columns = 3320 , 6
coeff = np.zeros((coeff_file_rows,coeff_file_columns,no_files),dtype = float)

for i in range(no_files):

    coeff_file_name = coeff_file_name_prefix + re_grace_names[i]
    coeff_pd_dataframe = pd.read_csv( coeff_file_name , 
            header = None,
            delimiter = '\s+',
            dtype = float)
    single_coeff_data = np.asarray(coeff_pd_dataframe , dtype = float )
    
    coeff[:,:,i] = single_coeff_data

coeff_rates = np.zeros((coeff_file_rows,coeff_file_columns) , dtype = float)
coeff_intercept = coeff_rates * 0 
coeff_r = coeff_rates * 0 
coeff_p = coeff_rates * 0 
coeff_std = coeff_rates * 0

for i in range(coeff_file_rows):
    coeff_rates[i,2],coeff_intercept[i,2],coeff_r[i,2],coeff_p[i,2],coeff_std[i,2] = linregress(ReTgrace,coeff[i,2,:])
    coeff_rates[i,3],coeff_intercept[i,3],coeff_r[i,3],coeff_p[i,3],coeff_std[i,3] = linregress(ReTgrace,coeff[i,3,:])
    coeff_rates[i,4],coeff_intercept[i,4],coeff_r[i,4],coeff_p[i,4],coeff_std[i,4] = linregress(ReTgrace,coeff[i,4,:])
    coeff_rates[i,5],coeff_intercept[i,5],coeff_r[i,5],coeff_p[i,5],coeff_std[i,5] = linregress(ReTgrace,coeff[i,5,:])
    
coeff_rates[:,0] = coeff[:,0,0]
coeff_rates[:,1] = coeff[:,1,0] 

np.savetxt(sys.argv[5]+sys.argv[4]+'_coeff_rates_'+station_name+'.txt',coeff_rates,fmt='%d\t%d\t%1.12e\t%1.12e\t%1.4e\t%1.4e')
print(station_name,'\t',
        "{0:.10f}".format(latitude) ,'\t', 
        "{0:.10f}".format(longitue) ,'\t', 
        "{:d}".format(data_flag.sum()),'\t' , 
        "{0:.6e}".format(gps_slope) ,'\t', 
        "{0:.6e}".format(gps_intercept) ,'\t', 
        "{0:.4f}".format(gps_r) ,'\t', 
        "{0:.4e}".format(gps_p) ,'\t', 
        "{0:.5e}".format(gps_std )) 
