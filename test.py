import numpy as np 

a = np.arange(20).reshape(4, 5)
b = np.arange(20).reshape(4, 5)
dis = np.sum(np.abs(a - b[1, :]), axis=1)
# print(a)
# print(b)
print(dis)
min_index = np.argmin(dis)
print(min_index)