This folder it to store and handel the GPS station time series data from MIT's ftp server.

All the time series are downloaded into folder raw/ by following command inside raw/
wget ftp://everest.mit.edu/pub/TimeSeries/ts_DFIX/*

The list of stations is stored in MIT_station.csv using the following command 

ls -all raw/*.mit.dfixd_frame.pos | awk '{ print substr($9 , 5 , 4) }' > MIT_station.csv
explanation: ls displays all the files in folder. ls -all displays all files with their details with 9th column as file name (combined with path). awk takes each row and gets the file name from 9th column as string. The station code is extracted by selecting a substring from file name string. And all the codes that will be printed are saved in MIT_station.csv.  And manually insert 'name' in the first line.

MIT_station_data file has the station codes with latitude and longitude
This file is created from the station_data.csv file from NGL data which has higher number of gps station (superset).
The following command is used, and refer cuonglm's answer in : https://unix.stackexchange.com/questions/125155/compare-two-files-for-matching-lines-and-store-positive-results
awk 'FNR==NR{a[$1];next}($1 in a){print}' MIT_station.csv station_data.csv > MIT_station_data.csv 

the shell script get_time_in_YYYY.YYYY.sh will make the GPS_data_* .txt file of all the stations from *.mit.dfixd_frame.pos files. GPS_data_* files are same as *.mit.dfixd_frame.pos files without header and with additional column in the beginning which is the decimal year. 
This decimal year is calculated by python script get_time_in_YYYY.py and get_time_in_YYYY.sh loops the python script for all the stations from MIT_station.csv file.

Before running get_time_in_YYYY.sh file copy all the *.mit.dfixd_frame.pos files from raw/ folder to this folder. This can be done by using following command in this folder
cp raw/*.mit.dfixd_frame.pos .
