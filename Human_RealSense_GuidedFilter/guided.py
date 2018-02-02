import numpy as np
from scipy import ndimage
import scipy.io
import matplotlib.pyplot as plt
import cv2
import copy
from guidedfilter import guidedfilter


cur_dir = "./img/2796/"

depth_img = cv2.imread(cur_dir + "distance.png", -1)

depth_mask = scipy.io.loadmat(cur_dir + "depth.mat")
depth_mask = depth_mask['x'][0]

'''
for i in range(len(depth_mask)):
	for j in range(len(depth_mask)):
		if depth_mask[i][j] == 1:
			depth_mask[i][j] = 1
		else:
			depth_mask[i][j] = 22 - depth_mask[i][j]
'''

x, y = np.where(depth_mask == 1)

for i in range(len(x)):
	depth_img[x[i]][y[i]] = 0

refined_img = guidedfilter(depth_mask, depth_img, r=40, eps=0.1)

final_img = copy.deepcopy(refined_img)

for i in range(len(final_img)):
	for j in range(len(final_img[0])):
		if final_img[i][j] < 0:
			final_img[i][j] = 0
		else:
			final_img[i][j] = final_img[i][j] * 20 / 256.0

save_name = "res_" + cur_dir[-5:-1] + ".jpg"
cv2.imwrite(save_name, final_img)


show_mat = cv2.imread(save_name, 0)
cv2.imshow("win", show_mat)
cv2.waitKey()