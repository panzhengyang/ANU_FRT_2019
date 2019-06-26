

rm GPS_data_* > /dev/null

#beginning of web address
webb="http://geodesy.unr.edu/gps_timeseries/tenv3/IGS08/"
# ending part of web address
webe=".IGS08.tenv3"


# help source
# https://www.cyberciti.biz/faq/unix-howto-read-line-by-line-from-file/

input="station.csv"
while IFS= read -r station
do
    echo
    echo Station : "$station"
    webaddress="$webb$station$webe"
    #echo Address : $webaddress
    wget $webaddress -O "GPS_data_$station.txt"
done < "$input"
