# refers : https://stackoverflow.com/questions/1469849/how-to-split-one-string-into-multiple-strings-separated-by-at-least-one-space-in
#           https://askubuntu.com/questions/442914/calculating-the-number-of-lines-in-a-file
#           https://www.cyberciti.biz/faq/bash-for-loop/
#           https://stackoverflow.com/questions/169511/how-do-i-iterate-over-a-range-of-numbers-defined-by-variables-in-bash
#           https://www.geeksforgeeks.org/write-bash-script-print-particular-line-file/
#           http://evc-cit.info/cit052/pass_to_awk.html

station_file="station_data.csv"
grace_names_file="names.txt"
grace_times_file="time_decimal_years.txt"

#rm GRACE_data_*  2> /dev/null   # removing any folder with same name with no error messages 

while IFS= read -r string
do

  # $string has spaces which needs to be split to station code lat and lon
  # example as follows
  #string="WARA -25.037 128.296"
  
  stringarray=($string)
  name=${stringarray[0]}
  lat=${stringarray[1]}
  lon=${stringarray[2]}
  
  #echo $name 
  #echo $lat
  #echo $lon

  string="$( wc -l $grace_names_file )"
  stringarray=($string)
  no_files=${stringarray[0]}    # number of files

  #for i in $(seq 1 1)
  for i in $(seq 1 $no_files)
  do

    shc_name="$(awk -v awk_i=$i 'NR==awk_i' $grace_names_file)"
    shc_time="$(awk -v awk_i=$i 'NR==awk_i' $grace_times_file)"
    #echo $shc_name $shc_time
    temp_file='temp.dat'
    #echo $lat $lon
    ./evaluate_sphrarm $shc_name $temp_file  $lat    -99      $lon     -99 10 edefn > /dev/null
    #echo $shc_time $(cat temp.dat) >> "$(pwd)/$grace_save_folder_name/$name.txt"
    echo $shc_time $(cat temp.dat) >> "GRACE_data_$name.txt"
    
    #echo $name $i

  done
  echo $name
done < "$station_file"
