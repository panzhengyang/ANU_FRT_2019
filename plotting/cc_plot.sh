# refer : http://gmt-tutorials.org/en/making_first_map.html
#         http://www.matthewwherman.com/documents/tutorials/gmt_tutorial_1.pdf
#         http://gmt.soest.hawaii.edu/doc/5.3.2/makecpt.html
#         http://gmt.soest.hawaii.edu/doc/5.3.2/gmt.conf.html

min_lon=105
max_lon=165
min_lat=-45
max_lat=-10
PSFILE="map.ps"
plot_width="50"   # in cm
margin_ratio="0.1"
title_space="5"     # in cm
data_file="cc.xy"
cpt_file="cc.cpt"
data_column="3"

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

#echo $PROJ
#echo $LIMS
#echo $XOFFSET
#echo $YOFFSET
#echo $ORIENTATION
#echo $common_additional_parameters

gmt pscoast $PROJ $LIMS -W0p -Dh -N1/0.25p -Gdarkseagreen2 -Scornflowerblue $XOFFSET $YOFFSET -K $ORIENTATION $common_additional_parameters > $PSFILE
gmt psbasemap $PROJ $LIMS -Bxa20g10 -Bya30g5 -BWeSn \
  -O -K $ORIENTATION $common_additional_parameters>> $PSFILE

gmt psxy $data_file $PROJ $LIMS -Sc0.25c -W0.25p -C$cpt_file -O $ORIENTATION $common_additional_parameters >> $PSFILE

open -a preview $PSFILE
#gs $PSFILE
