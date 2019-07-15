list_file=$1
python_output_file=$2
#list_file='./list.txt'
#python_output_file='./temp_test.txt'
mit_matrix_row_file_name_prefix='./matrix_row/mit_matrix_row_'
ngl_matrix_row_file_name_prefix='./matrix_row/ngl_matrix_row_'
matrix_row_file_name_suffix='.txt'
mit_slopes_file='./mit_above_50_slopes.txt'
ngl_slopes_file='./ngl_above_50_slopes.txt'
max_deg='4'
temp_python_input_file='temp_python_input.txt'
rm $temp_python_input_file 2> /dev/null

while IFS= read -r string
do 
  stringarray=($string)
  name=${stringarray[0]}
  lat=${stringarray[1]}
  lon=${stringarray[2]}
  code=${stringarray[3]}
  if [ $code == M ] 
  then
    matrix_row_file_name=$mit_matrix_row_file_name_prefix$name$matrix_row_file_name_suffix
    slopes_file_line="$( grep $name $mit_slopes_file )"
    slope="$(echo $slopes_file_line | awk '{print $5}')"
    no_points="$(echo $slopes_file_line | awk '{print $4}')"
    echo $matrix_row_file_name $slope $no_points >> $temp_python_input_file
  elif [ $code == N ]
  then
    matrix_row_file_name=$ngl_matrix_row_file_name_prefix$name$matrix_row_file_name_suffix
    slopes_file_line="$( grep $name $ngl_slopes_file )"
    slope="$(echo $slopes_file_line | awk '{print $5}')"
    no_points="$(echo $slopes_file_line | awk '{print $4}')"
    echo $matrix_row_file_name $slope $no_points >> $temp_python_input_file
  fi
done < $list_file

python ./do_lsf.py $temp_python_input_file $python_output_file $max_deg $3 $4

