# refer ninjagecko answer : https://stackoverflow.com/questions/6451655/python-how-to-convert-datetime-dates-to-decimal-years
from datetime import datetime as dt 
import time
import numpy as np
import pandas as pd 
import sys

station_code = sys.argv[1]
gps_data_file_name = 'raw/'+station_code +'.mit.dfixd_frame.pos'

#station_code = 'temp'
#gps_data_file_name = 'tmp.txt'


# these widths are based on the data file, unique for each file
mywidths = [ 5,2,2,3,2,2,12,15,15,15,9,8,9,7,7,7,21,15,10,13,10,10,11,8,9,7,7,7,6]

# in case of any errors
try:
    
    original_file = open(gps_data_file_name,'r')
    raw_file = original_file.read()
    original_file.close()
    start_index = raw_file.find('Start Field Description')
    end_index = raw_file.find('Reu  Soln') +10

    temp_data_file_name = 'temp_data.txt'
    temp_file = open(temp_data_file_name,'w')
    if ( start_index != -1 and end_index != -1 ):
        temp_file.write(raw_file.replace(raw_file[start_index:end_index],''))
    else :
        temp_file.write(raw_file)
    temp_file.close()
    
    pd_data = pd.read_fwf(temp_data_file_name,
            widths=mywidths,
            header = None,
            skiprows=9)

    np_data = np.asarray(pd_data)
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
except:
    # print only when there is an error
    # if something is printed then shell script can find failed stations
    print('1')
