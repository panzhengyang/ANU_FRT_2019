file="NGL_tmp.txt"
awk '{ lat=$2;lon=$3; if( ($12==0)  \
  && ($4>180) \
  \
  && (!( \
  ( (lon > 128)&&(lon<150)&&(lat>30)&&(lat<50) )  \
  || ( (lat < 67)&&(lat>60)&&(lon<-10)&&(lon>-25) ) \
  || ( (lat>-10)&&(lat<10)&&(lon<155)&&(lon>90) )  \
  ) ) \
  \
  &&( \
  ( (lat>60)&&(lon<-10)&&(lon>-75) )  \
  || ( (lat>50)&&(lon<-80)&&(lon>-120) )  \
  || ( (lon>5)&&(lon<40)&&(lat>50)) \
  || (lat<-60) \
  || ($7<10) \
  ) \
  ) {print $0}}' \
  ./NGL_result_2011.3333.txt > $file 
./locate.sh $file 8
  #&& ( (lat > 60)&&(lon > -75)&&(lon<-10)) \      
