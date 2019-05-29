# This script is to get the time stamps of each of the spherical harmonic coefficient files

# refer : https://www.learnshell.org/en/Basic_String_Operations
#         https://ryanstutorials.net/bash-scripting-tutorial/bash-arithmetic.php
#         https://stackoverflow.com/questions/12722095/how-do-i-use-floating-point-division-in-bash
#         https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-30.php
#         https://stackoverflow.com/questions/4651437/how-do-i-set-a-variable-to-the-output-of-a-command-in-bash

# for following command refer : https://stackoverflow.com/questions/15678796/suppress-shell-script-error-messages
rm time_decimal_years.txt 2> /dev/null

# start and end year index
syi=6
eyi=14

input='names.txt'
while IFS= read -r name
do
  # start and end years
  sy=${name:$syi:4}
  ey=${name:$eyi:4}

  # start day and end day
  sd=${name:$(expr $syi+4 ):3}    # There can be spaces inside (( ))
  ed=${name:$(expr $eyi+4 ):3} 
  
  # The leading zeros in start day and end day need to be stripted (eg: 012 to 12 )
  # This is required for later. Python does not consider 01 same as 1
  # refer : http://www.theunixschool.com/2013/03/how-to-remove-leading-zeros-in-string.html
  sd="$(echo $sd | sed 's/^0*//')"
  ed="$(echo $ed | sed 's/^0*//')"

  # using python since bash cannot handle floats
  # giving the expression to python (in python syntax) intrepreter and get the output from it

  #echo "print('{:.4f}'.format(($sy + $sd/365.0)))" | python
  #echo "print('{:.4f}'.format(($ey + $ed/365.0)))" | python 
  #echo "print('{:.4f}'.format( (($sy + $sd/365.0)+($ey + $ed/365.0))/2.0 ) )" | python

  ts="$( echo "print('{:.4f}'.format( (($sy + $sd/365.0)+($ey + $ed/365.0))/2.0 ) )" | python )"
  echo $ts

  # -e flag for considereing the \t or \n if there are any
  echo -e "$ts" >> time_decimal_years.txt
done < "$input"
