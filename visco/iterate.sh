./do_lsf.sh ./list.txt tmp_out_1.txt 
for i in $(seq 1 50)
do
  ip1="$( echo $i + 1 | bc -l )"
  ./calculate_Edot.sh "tmp_out_"$i".txt" list.txt "tmp_edot_"$i".txt"
  ./do_lsf.sh list.txt "tmp_out_"$ip1".txt" "do" "tmp_edot_"$i".txt"
  awk '(NR==2) { print $3 }' "tmp_out_"$ip1".txt"
done
