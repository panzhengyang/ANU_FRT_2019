# refer: https://stackoverflow.com/questions/29796979/read-line-containing-string-bash

input_file="MIT_decimal_year_successful_station.txt"
output_file="MIT_station_data.txt"
rm $output_file 2> /dev/null

while IFS= read -r name
do
  line="$(  awk '/NEU Reference position :/ { print $0 }' raw/$name".mit.dfixd_frame.pos" )"
  lat="$( echo $line | awk '{ print $5 }' )"
  lon="$( echo $line | awk '{ print $6 }' )"
  echo $name $lat $lon >> $output_file
done < $input_file

