
gps_suffix=".mit.dfixd_frame.pos"
faild_station_file="MIT_decimal_year_failed_station.txt"
successful_station_file="MIT_decimal_year_successful_station.txt"

rm $faild_station_file $successful_station_file 2> /dev/null

while IFS= read -r name
do
  echo doing for $name 

  # Here the python script runs and the print output from python is given to error_msg as well
  error_msg="$( python3 get_time_in_YYYY.YYYY.py $name )"
  
  if [ "$error_msg" == "1" ] 
  then
    echo $name >> $faild_station_file 
  else
    echo $name >> $successful_station_file
  fi
  echo
done < "MIT_station.csv"
