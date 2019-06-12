#refer :https://www.cyberciti.biz/faq/unix-linux-bash-script-check-if-variable-is-empty/
#       https://stackoverflow.com/questions/1378274/in-a-bash-script-how-can-i-exit-the-entire-script-if-a-certain-condition-occurs

plot_width="50"
margin_ratio="0.1"
title_space="1"

if [ -z $1 ]
then
  echo give something
  exit 1 
fi

temp_data_file="my_great_temp.xy"
awk '{print $3 " " $2}' $1 > $temp_data_file

min_lon="$( sort -k1 -n $temp_data_file | head -1 | awk '{ print $1 }' )"
max_lon="$( sort -k1 -n $temp_data_file | tail -1 | awk '{ print $1 }' )"
min_lat="$( sort -k2 -n $temp_data_file | head -1 | awk '{ print $2 }' )"
max_lat="$( sort -k2 -n $temp_data_file | tail -1 | awk '{ print $2 }' )"

PSFILE="temp.ps"

wh_ratio="$( echo "print(float($max_lon-$min_lon)/float($max_lat-$min_lat)) " | python )"
page_width="$( echo "print( float($plot_width)*(1.0 + 2.0*($margin_ratio)) )" | python )"
plot_height="$( echo "print(float($plot_width)/$wh_ratio) " | python )"
page_height="$( echo "print( float($plot_height)*(1.0 + 2.0*($margin_ratio)) + float($title_space) )" | python )"
x_offset="$( echo "print( (float($page_width)-float($plot_width))/2 )" | python )"
y_offset="$( echo "print( (float($page_height)-float($title_space)-float($plot_height))/2 )" | python )"

PROJ="-JQ$plot_width""c"
LIMS="-R$min_lon/$max_lon/$min_lat/$max_lat"
XOFFSET="-X$x_offset""c"
YOFFSET="-Y$y_offset""c"
ORIENTATION="-P"
common_additional_parameters="--PS_MEDIA=$page_width""c""x$page_height""c"
#pscoast_parameters="-Gdarkseagreen2 -Scornflowerblue -W0p -Dh -N1/0.25p"
pscoast_parameters="-W0p -Dh -N1/0.05p"

gmt pscoast $PROJ $LIMS $pscoast_parameters $XOFFSET $YOFFSET -K $ORIENTATION $common_additional_parameters > $PSFILE
gmt psbasemap $PROJ $LIMS -Bxa20g10 -Bya30g5 -BWeSn \
    -O -K $ORIENTATION $common_additional_parameters>> $PSFILE

gmt psxy $temp_data_file $PROJ $LIMS -Sc0.1c -W0.25p -Gred -O $ORIENTATION $common_additional_parameters >> $PSFILE

open -a preview $PSFILE
rm $temp_data_file 2> /dev/null
