# refer : http://gmt-tutorials.org/en/making_first_map.html
#         http://www.matthewwherman.com/documents/tutorials/gmt_tutorial_1.pdf
#         http://gmt.soest.hawaii.edu/doc/5.3.2/makecpt.html
#         http://gmt.soest.hawaii.edu/doc/5.3.2/gmt.conf.html
#         https://stackoverflow.com/questions/8654051/how-to-compare-two-floating-point-numbers-in-bash
#         https://www.tim-dennis.com/data/tech/2016/08/09/using-awk-filter-rows.html
#         https://stackoverflow.com/questions/19075671/how-do-i-use-shell-variables-in-an-awk-script

min_lon=105
max_lon=165
min_lat=-45
max_lat=-10
PSFILE="map.ps"
plot_width="50"   # in cm
margin_ratio="0.1"
title_space="1"     # in cm
data_file="rms_gps.xy"
data_column="3"
min_value=0
max_value=20    # maximum value of rms for makecpt

temp_cpt_file="tmp.cpt"
temp_data_file="temp.xy"
rm $temp_cpt_file $temp_data_file 2> /dev/null

awk -v awk_max_lat="$max_lat" -v awk_min_lat="$min_lat" -v awk_max_lon=$max_lon -v awk_min_lon=$min_lon \
  '{ if( ($1 < awk_max_lon) && ($1 > awk_min_lon) && ($2 < awk_max_lat) && ($2 > awk_min_lat) ) { print } }' \
  $data_file > $temp_data_file

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
pscoast_parameters="-W0p -Df -N1/0.05p"

#echo $PROJ
#echo $LIMS
#echo $XOFFSET
#echo $YOFFSET
#echo $ORIENTATION
#echo $common_additional_parameters

gmt pscoast $PROJ $LIMS $pscoast_parameters $XOFFSET $YOFFSET -K $ORIENTATION $common_additional_parameters > $PSFILE
gmt psbasemap $PROJ $LIMS -Bxa20g10 -Bya30g5 -BWeSn \
  -O -K $ORIENTATION $common_additional_parameters>> $PSFILE

#gmt makecpt -Cpolar -E10000 -i2 $temp_data_file > $temp_cpt_file
gmt makecpt -Cpolar -T$min_value/$max_value/1000+ > $temp_cpt_file

gmt psxy $temp_data_file $PROJ $LIMS -Sc0.25c -W0.25p -C$temp_cpt_file -O $ORIENTATION $common_additional_parameters >> $PSFILE

rm $temp_cpt_file $temp_data_file 2> /dev/null
open -a preview $PSFILE
#gs $PSFILE
