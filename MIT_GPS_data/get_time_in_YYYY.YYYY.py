# refer ninjagecko answer : https://stackoverflow.com/questions/6451655/python-how-to-convert-datetime-dates-to-decimal-years
from datetime import datetime as dt 
import time
import numpy as np
import pandas as pd 
import sys

station_code = sys.argv[1]
gps_data_file_name = 'raw/'+station_code +'.mit.dfixd_frame.pos'

# these widths are based on the data file, unique for each file
mywidths = [ 5,2,2,3,2,2,12,15,15,15,9,8,9,7,7,7,21,15,10,13,10,10,11,8,9,7,7,7,6]
pd_data = pd.read_fwf(gps_data_file_name,
        widths=mywidths,
        header = None,
        skiprows=37)

np_data = np.asarray(pd_data)
print(np.shape(np_data))
year_array = np_data[:,0]
month_array = np_data[:,1]
day_array = np_data[:,2]
hour_array = np_data[:,3]
minute_array = np_data[:,4]
second_array = np_data[:,5]

decimal_year = np.zeros(np.size(year_array))

def sinceEpoch(mydatetime):
    return time.mktime(mydatetime.timetuple())

for i in range( np.size(year_array)):
    
    mydatetime = dt(year_array[i],month_array[i],day_array[i],hour_array[i],minute_array[i],second_array[i]) 
    
    year = mydatetime.year
    startOfThisYear = dt(year = year , month = 1 , day = 1)
    startOfNextYear = dt(year = year+1 , month = 1 , day = 1)
    
    yearElapsed = sinceEpoch(mydatetime) - sinceEpoch(startOfThisYear)
    yearDuration = sinceEpoch(startOfNextYear) - sinceEpoch(startOfThisYear)
    fraction = yearElapsed / yearDuration

    decimal_year[i] = mydatetime.year + fraction

np.savetxt('GPS_data_'+station_code+'.txt',
        np.column_stack((decimal_year,np_data)),
        fmt='%.8f %d %d %d %d %d %d %.4f %.5f %.5f %.5f %.5f %.5f %.5f %.3f %.3f %.3f %.10f %.10f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.3f %.3f %.3f %s')
