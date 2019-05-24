
myfile = open('all_stations.txt','r')
text = myfile.read()
myfile.close()
split_list = text.split()
joined_list = '\n'.join(split_list)
station_file = open('station.csv','w')
station_file.writelines(joined_list)
station_file.close()
