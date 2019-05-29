# This code is to preprocess the coefficient files into a particular format so that fortran code that calculates the displacements can read it 
# The data should be changed into a format where number of columsn is 6 i.e. deg , order , C , S , sigmaC , simgaS (2nd to 7th column in original file, excluding the first ans last two columsn) and seperated by space

import numpy as np
import pandas as pd
from subprocess import call

names_file = 'names.txt'
tar_gz_file_name = 'GRGS_anomaly.tar.gz'

# remove the existing extracted files and freshly extract again
call('rm GSM-* 2> /dev/null',shell=True)
call('tar xvzf '+tar_gz_file_name , shell=True)

my_file = open(names_file,'r')
raw = my_file.read()
my_file.close()

# list of all the file names
names = raw.split()

# Original data is not delimited and should be seperated from the following column numbers
mywidths = [8, 5, 3, 19, 19, 11, 11, 14, 14]

for filename in names :
    data = pd.read_fwf(filename,widths=mywidths,header=None,skiprows=3)
    np_data = np.asarray(data)
    np.savetxt(filename,np_data[:,1:7],fmt='%d %d %1.12e %1.12e %1.4e %1.4e')
    print('saved the file : '+filename)

