# import requests
web1 = 'http://geodesy.unr.edu/NGLStationPages/stations/'
web2 = '.sta'

file_name = 'station.csv'
my_file = open(file_name,'r')
raw_data = my_file.read()
name = raw_data.split()
my_file.close()

s = open('station_data.csv','a')    # file to store data if lat lon are obtained successsfully
f = open('failed_stations.csv','a') # file to store station names where lat lon are not obtained due to what ever reason

sn = 0      # number of successful retrevals
fn = 0      # number of failed retrevals


for i in range(5) :
    print('nothing')
    web_address = web1 + name[i] + web2
    
    try :
        page = requests.get(web_address)
    except : pass

