Steps carried out: 

sorting the data based on rms values of gps in ascending order since some gps station rms values are anomalous. refer : https://stackoverflow.com/questions/6438896/sorting-data-based-on-second-column-of-a-file

Removing the lines which correspond to failed comparisions. refer: https://www.tim-dennis.com/data/tech/2016/08/09/using-awk-filter-rows.html

columns
station_code = 1
Lat =2
Lon = 3
no_of_data_points = 4
rms_gps = 5
rms_grace = 6
rms_diff = 7
slope_gps = 8
slope_grace = 9
slope_diff = 10
corr_coeff = 11
error_message = 12
