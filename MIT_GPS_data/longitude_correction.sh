mit_data_file=$1

mit_temp_backup_file="tmp_mit_station_data.txt"
cp ./$mit_data_file ./$mit_temp_backup_file
rm $mit_data_file
while IFS= read -r string
do
  stringarray=($string)
  lon=${stringarray[2]}

  stringarray[2]="$( echo "$lon -360.0*($lon>180.0)" | bc -l  )"
  echo ${stringarray[@]}  >> $mit_data_file
done < $mit_temp_backup_file

