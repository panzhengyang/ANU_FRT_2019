import requests

web1 = 'http://geodesy.unr.edu/NGLStationPages/stations/'
web2 = '.sta'

file_name = 'station.csv'
my_file = open(file_name,'r')
raw_data = my_file.read()
name = raw_data.split()
my_file.close()

sname = 'station_data.csv'
fname = 'failed_lat_lon_stations.csv'
s = open(sname,'w')    # file to store data if lat lon are obtained successsfully
f = open(fname,'w') # file to store station names where lat lon are not obtained due to what ever reason

s.write( 'name' + '\t' + 'lat' + '\t' + 'lon' + '\n')
s.close()
f.write( 'name' + '\t' + 'code' + '\n')
f.close()

sn = 0      # number of successful retrevals
fn = 0      # number of failed retrevals
tn = len(name)  # total number of stations

print('\n\n')
#for i in range(5) :
for i in range(tn):
    
    web_address = web1 + name[i] + web2
    
    try :
        page = requests.get(web_address)
        if(page.status_code == 200):
            text = page.text
            
            lat_index = text.find('Latitude')
            lon_index = text.find('Longitude')
            if (lat_index != -1 and lon_index != -1):
                
                lat_string = text[lat_index+9:lat_index+30]
                lon_string = text[lon_index+10:lon_index+30]
                
                lat_string = lat_string[:lat_string.find('<')]
                lon_string = lon_string[:lon_string.find('</h4')]
                
                lat = float(lat_string)
                lon = float(lon_string)
                
                s = open(sname,'a')
                s.write( name[i] + '\t' + str(lat) + '\t' + str(lon) + '\n')
                s.close()
                sn += 1
                
            else : 
                print('Did not find lat lon for : ' + name[i] )
                f = open(fname,'a')
                f.write( name[i] + '\t' + '1' + '\n' )    # 1 when lat lon are not found
                f.close()
                fn += 1
        else:
            print('did not get page for : ' + name[i])
            f = open(fname,'a')
            f.write( name[i] + '\t' + '2' + '\n')   # 2 for not able to get the page
            f.close()
            fn += 1
    except : 
        print('requests error for ' + name[i])
        f = open(fname,'a')
        f.write( name[i] + '\t' + '3' + '\n')   # 3 for requests error
        f.close()
        fn += 1

    print('\tSuccessful\t:\t'+str(sn)+'/'+str(tn)+'\t\tFalied\t:\t'+str(fn)+'/'+str(tn))


print('\n\n')
print("\tNumber of Success\t:\t"+str(sn))
print("\tNumber of failures\t:\t"+str(fn))
print('\n\n')
