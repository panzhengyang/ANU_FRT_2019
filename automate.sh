
gps_prefix="GPS_data/GPS_data_"
grace_prefix="GRACE_data/GRACE_data_"
station_data_file="station_data.csv"
result_file_name="result.txt"

rm $result_file_name > /dev/null
echo "Station_code Lat Lon rms_gps rms_grace rms_gps_grace corr_coeff" >> $result_file_name

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
  
  echo -e "$name\t$lat\t$lon\t$result" 
  echo -e "$name\t$lat\t$lon\t$result" >> $result_file_name

done < "$station_data_file"

