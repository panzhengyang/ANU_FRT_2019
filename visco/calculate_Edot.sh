
coeff_file=$1
Edot_file=$3
list_file=$2

#coeff_file='./visco_coeff_mit_above_50.txt'
#Edot_file='./Edot_mit_above_50.txt'
#list_file='./list.txt'
rm $Edot_file 2> /dev/null
while IFS= read -r string
do
  stringarray=($string)
  name=${stringarray[0]}
  lat=${stringarray[1]}
  lon=${stringarray[2]}

  #python3 -W ignore ./my_evaluate_sphharm.py $coeff_file $lat $lon >> $Edot_file
  
  ./evaluate_sphharm $coeff_file temp.dat $lat -99 $lon -99 1 edefn > /dev/null
  elastic="$( awk '{ print $5/1000.0 }' temp.dat )"
  ./evaluate_sphharm $coeff_file temp.dat $lat -99 $lon -99 1 visco > /dev/null
  visco_elastic="$( awk '{ print $3/1000.0 }' temp.dat )"
  echo "$visco_elastic $elastic" | awk '{ print $1-$2 }' >> $Edot_file


#  echo $name $lat $lon
done < $list_file 
