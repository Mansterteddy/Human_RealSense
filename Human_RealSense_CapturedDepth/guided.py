import numpy as np
from scipy import ndimage
import scipy.io
import matplotlib.pyplot as plt
import cv2


cur_dir = "./img/2796/"
predicted_depth_filename = cur_dir + "depth.mat"
captured_depth_filename = cur_dir + "distance.png"

predicted_depth_mat = scipy.io.loadmat(predicted_depth_filename)
predicted_depth_mat = predicted_depth_mat['x'][0]

captured_depth_mat = cv2.imread(captured_depth_filename, -1)
#for i in range(3):
 #   captured_depth_mat = ndimage.median_filter(captured_depth_mat, 3)

for i in range(len(captured_depth_mat)):
    for j in range(len(captured_depth_mat[0])):
            if predicted_depth_mat[i][j] == 1:
            	captured_depth_mat[i][j] = 0
            else:
	            captured_depth_mat[i][j] = captured_depth_mat[i][j] * 10 / 256.0

cv2.imwrite("res.jpg", captured_depth_mat)
