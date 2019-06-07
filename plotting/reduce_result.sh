# This script is to extract just the lat lon and correlation coefficients from result.txt into a form where GMT can use it

file_name="result.txt"
out_file_name="rms_gps_grace.xy"
rm $out_file_name 2> /dev/null

while IFS= read -r string
do
  stringarray=($string)
  lat=${stringarray[1]}
  lon=${stringarray[2]}
  no_data=${stringarray[3]}
  mydata=${stringarray[6]}
  em=${stringarray[8]}
  
  if [ $em -eq 0 ]
  then
    echo $lon $lat $mydata $no_data >> $out_file_name
  fi
done < $file_name

