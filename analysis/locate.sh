#refer :https://www.cyberciti.biz/faq/unix-linux-bash-script-check-if-variable-is-empty/
#       https://stackoverflow.com/questions/1378274/in-a-bash-script-how-can-i-exit-the-entire-script-if-a-certain-condition-occurs

plot_width="50"
margin_ratio="0.5"
title_space="2"
title="Title"
bottom_space="4"
min_value="0"
max_value="10"

if [ -z $2 ]
then
  echo give something
  exit 1 
fi

temp_cpt_file="my_great_temp.cpt"
temp_data_file="my_great_temp.xy"
awk -v awk_var=$2 '{print $3 " " $2 " " $awk_var}' $1 > $temp_data_file

min_lon="$( sort -k1 -n $temp_data_file | head -1 | awk '{ print $1 }' )"
max_lon="$( sort -k1 -n $temp_data_file | tail -1 | awk '{ print $1 }' )"
min_lat="$( sort -k2 -n $temp_data_file | head -1 | awk '{ print $2 }' )"
max_lat="$( sort -k2 -n $temp_data_file | tail -1 | awk '{ print $2 }' )"

#max_value="$( sort -k$2 -n $temp_data_file | tail -1 | awk '{ print $3 }' )"
#min_value="$( sort -k$2 -n $temp_data_file | head -1 | awk '{ print $3 }' )"

PSFILE="temp.ps"

wh_ratio="$( echo "print(float($max_lon-$min_lon)/float($max_lat-$min_lat)) " | python )"
page_width="$( echo "print( float($plot_width)*(1.0 + 2.0*($margin_ratio)) )" | python )"
plot_height="$( echo "print(float($plot_width)/$wh_ratio) " | python )"
page_height="$( echo "print( float($plot_height)*(1.0 + 2.0*($margin_ratio)) + float($title_space) + float($bottom_space) )" | python )"
x_offset="$( echo "print( (float($page_width)-float($plot_width))/2 )" | python )"
y_offset="$( echo "print( (float($page_height)-float($title_space)+float($bottom_space)-float($plot_height))/2 )" | python )"

PROJ="-JQ$plot_width""c"
LIMS="-R$min_lon/$max_lon/$min_lat/$max_lat"
XOFFSET="-X$x_offset""c"
YOFFSET="-Y$y_offset""c"
ORIENTATION="-P"
common_additional_parameters="--PS_MEDIA=$page_width""c""x$page_height""c"
#pscoast_parameters="-Gdarkseagreen2 -Scornflowerblue -W0p -Dh -N1/0.25p"
pscoast_parameters="-W0p -Dc -A10000 -N1/0.05p -BWSNE+t$title"

gmt pscoast $PROJ $LIMS $pscoast_parameters $XOFFSET $YOFFSET -K $ORIENTATION $common_additional_parameters > $PSFILE
gmt psbasemap $PROJ $LIMS -Bxa20g10 -Bya30g5 -BWeSn \
    -O -K $ORIENTATION $common_additional_parameters>> $PSFILE

gmt makecpt -Cpolar -T$min_value/$max_value/500+ > $temp_cpt_file
gmt psxy $temp_data_file $PROJ $LIMS -Sc0.25c -W0.25p -C$temp_cpt_file -O -K $ORIENTATION $common_additional_parameters >> $PSFILE

scale_yoffset=$(echo -$bottom_space/2 | bc -l )
gmt psscale $common_additional_parameters -C$temp_cpt_file -Ba -O -Dx0c/"$scale_yoffset"c+w"$plot_width"c/0.5c+h  -P >> $PSFILE

open -a preview $PSFILE
rm $temp_data_file $temp_cpt_file 2> /dev/null
