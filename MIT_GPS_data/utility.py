from datetime import datetime as dt
import time
import numpy as np

# refer ninjagecko answer : https://stackoverflow.com/questions/6451655/python-how-to-convert-datetime-dates-to-decimal-years
def toYearFraction(date_array,time_array):
    out = np.zeros(np.size(date_array))
    for i in range( np.size(date_array) ):
        raw_date = date_array[i]
        raw_time = time_array[i]
        
        raw_year = int( str(raw_date)[0:4] )
        raw_month = int( str(raw_date)[4:6] )
        raw_day = int( str(raw_date)[6:8] )
        raw_hour = int( str(raw_time)[0:2] )
        raw_minute = int( str(raw_time)[2:4] )
        raw_second = int( str(raw_time)[4:8] ) 
        
        date = dt(raw_year,raw_month,raw_day,raw_hour,raw_minute,raw_second)
        
        def sinceEpoch(date):
            return time.mktime(date.timetuple())
        s = sinceEpoch
        
        year = date.year
        startOfThisYear = dt(year = year , month = 1 , day = 1)
        startOfNextYear = dt(year = year+1 , month = 1 , day = 1)

        yearElapsed = s(date) - s(startOfThisYear)
        yearDuration = s(startOfNextYear) - s(startOfThisYear)
        fraction = yearElapsed/yearDuration

        out[i] = date.year + fraction

    return out



