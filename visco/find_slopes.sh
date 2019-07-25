input_file='./filtered_only_ngl.txt'
out_file='./filtered_only_ngl_slopes.txt'
gps_data='ngl'
save_path='./coeff_rate/'
rm $out_file 2> /dev/null 
#echo station lat lon no_points slope intercept r_value p_value standard_deviation > $out_file 
while IFS= read -r string
do
  stringarray=($string)
  name=${stringarray[0]}
  lat=${stringarray[1]}
  lon=${stringarray[2]}

  python3 -W ignore find_slopes.py $name $lat $lon $gps_data $save_path >> $out_file 
  
  echo done for $name only_ngl 

done < $input_file 
