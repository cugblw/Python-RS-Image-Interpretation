import numpy as np

array_3d = np.zeros((3,5,5))

# print(array_3d)


band1 = np.zeros((5,5))
band2 = np.zeros((5,5))
band3 = np.zeros((5,5))

rgb = np.dstack([band1,band2,band3])
# print(rgb)

# if array_3d == rgb:
#     print("{} equal {}.".format("array_3d","rgb"))