
gps_prefix="MIT_GPS_data/GPS_data_"
grace_prefix="GRACE_data/GRACE_data_"
station_data_file="MIT_station_data.txt"
result_file_name="MIT_result_2011.3333.txt"
failed_station_file_name="MIT_failed_stations.txt"

#rm $result_file_name 2> /dev/null
#rm $failed_station_file_name 2> /dev/null
echo "Station_code Lat Lon no_of_data_points rms_gps rms_grace rms_diff slope_gps slope_grace slope_diff corr_coeff error_message" >> $result_file_name

while IFS= read -r string
do
  stringarray=($string)
  name=${stringarray[0]}
  lat=${stringarray[1]}
  lon=${stringarray[2]}
  
  #echo $name
  #echo $lat 
  #echo $lon

  result="$( python3 -W ignore compare.py "$grace_prefix$name.txt" "$gps_prefix$name.txt")"
  
  error_code="${result: -1}"    # the last character in the string
  
  #echo $error_code  
  if [ $error_code -eq 2 ]
  then
    echo -e "Error : $name\t$lat\t$lon"
    echo -e "$name\t$lat\t$lon" >> $failed_station_file_name
  else
    echo -e "$name\t$lat\t$lon\t$result" 
    echo -e "$name\t$lat\t$lon\t$result" >> $result_file_name
  fi
done < "$station_data_file"

