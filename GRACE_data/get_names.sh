# refer : https://unix.stackexchange.com/questions/17064/how-to-print-only-last-column

# for following command refer : https://stackoverflow.com/questions/15678796/suppress-shell-script-error-messages
rm names.txt 2> /dev/null

input='list.txt'
while IFS= read -r line
do
#  echo $line
  echo $line | awk '{print $NF}' >> names.txt
done < "$input"
