import numpy as np
from utility import toYearFraction as tyf 

d = np.array([20190808 , 20190808])
t = np.array([141414 , 141415])

bla= tyf(d,t)
print('%.10f %.10f' % (bla[0] , bla[1]))
