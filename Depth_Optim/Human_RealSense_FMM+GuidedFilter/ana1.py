import scipy.io
import os
import cv2
import numpy as np
import copy
from scipy import ndimage


file_name = "debug 2.jpg"


mat = cv2.imread(file_name, 0)
print("val: ", mat[40][130])
cv2.imshow("Mat", mat)
cv2.waitKey()