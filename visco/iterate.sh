# $2 is the degree of lsf
degree=$2
# $1 is the file name of the station list 
list_file=$1
./do_lsf.sh $list_file tmp_out_1.txt $degree 
cp tmp_out_1.txt "deg_"$degree".txt"
echo "first calc over with"
awk '(NR==2) { print $3 }' tmp_out_1.txt
./calculate_Edot.sh tmp_out_1.txt $list_file tmp_edot_1.txt
./do_lsf.sh $list_file tmp_out_2.txt $degree "do" tmp_edot_1.txt no_need
awk '(NR==2) { print $3 }' tmp_out_2.txt
for i in $(seq 2 50)
do
  ip1="$( echo $i + 1 | bc -l )"
  im1="$( echo $i - 1 | bc -l )"
  ./calculate_Edot.sh "tmp_out_"$i".txt" $list_file "tmp_tmp_edot_"$i".txt"
  paste "tmp_tmp_edot_"$i".txt" "tmp_edot_"$im1".txt" | awk '{ print $1+$2 }' > "tmp_edot_"$i".txt"
  rm "tmp_tmp_edot_"$i".txt"
  ./do_lsf.sh $list_file "tmp_out_"$ip1".txt" $degree "do" "tmp_edot_"$i".txt" no_need
  awk '(NR==2) { print $3 }' "tmp_out_"$ip1".txt"
done
