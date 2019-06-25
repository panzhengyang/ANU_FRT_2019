
The .tar.gz file has the spherical harmonic coefficients' anomaly at different time periods. 

tar -ztvf GRGS_anomaly.tar.gz 
is used to list all the file names in the .tar.gz file. The output also includes the details along with just the file names

tar -ztvf GRGS_anomaly.tar.gz > list.txt 
is used to save all the output from the previous command into a text file

the shell script extracts the file names from the output of previous command and saves them in another file called names.txt

To extract all the files use
tar xvzf GRGS_anomaly.tar.gz 

The time stamps of each coefficient file is obtained from the file name and stored in time_decimal_years.txt by the script get_time_stamps.sh

The station_data.csv file is copied here and the first line which contains the header is deleted manually
The station_data.csv file has the info about the lat lon at which the GRACE elastic deformation time series is required. 

get_GRACE_lat_lon_time_series.sh runs the fortran executable which takes the spherical harmonic coeff files and generates the time series at different lat lon.

The MIT data has few stations which are no present in the NDL data. So GRACE data is generated for those additional stations. 
These stations' list is prepared as follows and edited in the get_GRACE_lat_lon_time_series.sh file. Also the remove statement is commented in .sh file. 
awk 'NR==FNR {a[$1];next}!($1 in a)' station_data.csv MIT_station_data.txt > additional_MIT_station.txt
refer Don Kepler Brian's answer : https://stackoverflow.com/questions/32481877/what-is-nr-fnr-in-awk/32482224 
There is a change made in the presend usage. $0 is changed to $1 since matching is done only for first column.

Not the spherical harmonic coefficient files are extracted and get_GRACE_lat_lon_time_series.sh is run. 
