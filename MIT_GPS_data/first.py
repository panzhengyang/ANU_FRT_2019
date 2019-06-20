import numpy as np
from utility import toYearFraction as tyf 

d = np.array([20190808 , 20000808])
t = np.array([141414 , 141414])

print(tyf(d,t))
