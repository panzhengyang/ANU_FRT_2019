import numpy as np
from pandas import read_csv
from sys import argv

data_pd_dataframe = read_csv(argv[1],
        skiprows = 1,
        header = None,
        sep='\s+')
matrix_row_file_name = np.asarray(data_pd_dataframe.iloc[:,0])
no_points = np.asarray(data_pd_dataframe.iloc[:,2],dtype=float)
slope = np.asarray(data_pd_dataframe.iloc[:,1],dtype=float)

max_deg = argv[3] 

tmp_data = np.asarray( read_csv( matrix_row_file_name[0],
    header = None,
    sep = '\s+',
    dtype = float ))
matrix = tmp_data[:,2]
n = tmp_data[:,0]
m = tmp_data[:,1]

size = np.size(name)

for i in np.linspace(1, size -1, size-1, dtype = int):
    row = np.asarray( read_csv( matrix_row_file_name[i],
        header = None,
        sep = '\s+',
        dtype = float ))[:,2]
    matrix = np.column_stack((matrix,row))

Edot = matrix[0,:]
max_index = int( (max_deg+max_deg*(max_deg+1)/2)*2-4 )        # which includes sin terms with order m = 0
n = n[1:max_index+1]
m = m[1:max_index+1]
matrix = matrix[1:max_index+1,:]
tmp_index = np.linspace(0,np.size(m)-1,np.size(m),dtype=int)
tmp_flag = (tmp_index*0 + 1).astype(bool)       # default True
tmp_flag[  tmp_index[m==0][1::2]  ] = False
n = n[tmp_flag]
m = m[tmp_flag]
matrix = matrix[tmp_flag,:]

A = np.asmatrix( matrix ).T
b = np.asmatrix( slope - Edot ).T
print('starting matrix inversion')
AtAwi = (A.T*A).I
print('done matrix inversion')
x = AtAwi * A.T * b
estimates = np.asarray(x)
print(AtAwi)
tmp_index = np.linspace(0,np.size(m)-1,np.size(m),dtype=int)
tmp_flag = (tmp_index*0).astype(bool)       # default False
tmp_flag[ m == 0 ] = True
insert_index = tmp_index[tmp_flag] + 1
n = np.insert(n,insert_index,n[tmp_flag])
m = np.insert(m,insert_index,m[tmp_flag])
estimates = np.insert(estimates,insert_index,0)

np.savetxt(argv[2],
        np.column_stack((n[0::2],m[0::2],estimates[0::2],estimates[1::2])),
        fmt='%d %d %1.12e %1.12e 0.0000e+00 0.0000e+00')
