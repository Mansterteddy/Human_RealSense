import numpy as np
from scipy import ndimage
import scipy.io
import matplotlib.pyplot as plt
import cv2


cur_dir = "./img/2796/"

depth_mask = scipy.io.loadmat(cur_dir + "depth.mat")
depth_mask = depth_mask['x'][0]

for i in range(len(depth_mask)):
	for j in range(len(depth_mask)):
		depth_mask[i][j] = 21 - depth_mask[i][j]

final_mask = depth_mask

for i in range(len(final_mask)):
	for j in range(len(final_mask[0])):
		if(final_mask[i][j] == 20):
			final_mask[i][j] = 0
		else:
			final_mask[i][j] = final_mask[i][j] * 10

cv2.imwrite("res.jpg", final_mask)
