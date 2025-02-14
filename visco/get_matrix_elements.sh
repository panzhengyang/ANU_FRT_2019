
input_file_name='./filtered_additional_NGL_greenland_110_slopes.txt'

python_input_file_prefix='./coeff_rate/ngl_coeff_rates_'
python_input_file_suffix='.txt'
python_output_file_prefix='matrix_row/ngl_matrix_row_'
python_output_file_suffix='.txt'

while IFS= read -r string
do
  stringarray=($string)
  name=${stringarray[0]}
  lat=${stringarray[1]}
  lon=${stringarray[2]}

  python -W ignore get_matrix_elements.py $python_input_file_prefix$name$python_input_file_suffix $python_output_file_prefix$name$python_output_file_suffix $lat $lon 
  echo $name only ngl
done < $input_file_name 
