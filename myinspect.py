import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import matplotlib.image as mpimg

data = pd.read_csv('result.txt',sep='\s+')

np_data = np.asarray(data.iloc[:,1:],dtype=float)
station = np.asarray(data.iloc[:,0])
print(station)
print(np.shape(np_data))

lat , lon , dp , rms_gps , rms_grace , rms_gps_grace , cc , em = np_data[:,0].astype(float) , np_data[:,1].astype(float) , np_data[:,2].astype(float) , np_data[:,3].astype(float) , np_data[:,4].astype(float) , np_data[:,5].astype(float) , np_data[:,6].astype(float) , np_data[:,7].astype(float) 

image = mpimg.imread("mymap.png")
plt.imshow(image,extent=[-180,180,90,-90])
plt.show()
