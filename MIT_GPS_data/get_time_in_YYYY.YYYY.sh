
gps_suffix=".mit.dfixd_frame.pos"

while IFS= read -r name
do
  echo doing for $name 
  python3 get_time_in_YYYY.YYYY.py $name
  echo
  echo
  echo
done < "MIT_station.csv"
