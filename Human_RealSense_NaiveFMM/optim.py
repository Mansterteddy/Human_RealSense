import scipy.io
import os
import cv2
import numpy as np
import copy
from scipy import ndimage
from guidedfilter import guidedfilter

# Calculate Gradients
def calcGradient():
    gradient = 45
    return gradient

# Remove Outliers in captured depth
def removeOutliers(humanbody_x, humanbody_y, captured_depth_mat):

    depth_range = 900

    captured_depth_nozeros = []

    for i in range(len(humanbody_x)):
        x_pos = humanbody_x[i]
        y_pos = humanbody_y[i]

        if(captured_depth_mat[x_pos][y_pos] != 0):
            captured_depth_nozeros.append(captured_depth_mat[x_pos][y_pos])

    captured_depth_nozeros_array = np.array(captured_depth_nozeros)
    mean_depth = np.mean(captured_depth_nozeros_array)
    min_depth = mean_depth - depth_range
    max_depth = mean_depth + depth_range
    print("min_depth: ", min_depth)
    print("max_depth: ", max_depth)

    captured_depth_x = []
    captured_depth_y = []

    for i in range(len(humanbody_x)):
        cur_x_pos = humanbody_x[i]
        cur_y_pos = humanbody_y[i]
        cur_depth = captured_depth_mat[cur_x_pos][cur_y_pos]

        if(cur_depth != 0 and cur_depth > min_depth and cur_depth < max_depth):
            captured_depth_x.append(cur_x_pos)
            captured_depth_y.append(cur_y_pos)

    print("captured depth len: ", len(captured_depth_x), len(captured_depth_y))

    return captured_depth_x, captured_depth_y

# Calculate pixels with different distance to captured data
def calcDistance(predicted_depth_mat, captured_depth_mat):

    humanbody_x, humanbody_y = np.where(predicted_depth_mat != 1)
    print("human pixel len: ", len(humanbody_x))

    captured_sample_x, captured_sample_y = np.where(captured_depth_mat != 0)
    print("captured sample len: ", len(captured_sample_x))

    captured_depth_x, captured_depth_y = removeOutliers(humanbody_x, humanbody_y, captured_depth_mat)

    flag_dict = {}
    for i in range(len(humanbody_x)):
        x_pos = humanbody_x[i]
        y_pos = humanbody_y[i]
        pos = (x_pos, y_pos)
        flag_dict[pos] = 0

    for i in range(len(captured_depth_x)):
        x_pos = captured_depth_x[i]
        y_pos = captured_depth_y[i]
        pos = (x_pos, y_pos)
        flag_dict[pos] = 1


    list_x = copy.deepcopy(captured_depth_x)
    list_y = copy.deepcopy(captured_depth_y)
    dist_x = []
    dist_y = []
    dist_x.append(captured_depth_x)
    dist_y.append(captured_depth_y)

    while len(list_x) != len(humanbody_x):
        cur_list_x = dist_x[-1]
        cur_list_y = dist_y[-1]

        append_x = []
        append_y = []

        for i in range(len(cur_list_x)):
            x_axis = cur_list_x[i]
            y_axis = cur_list_y[i]

            x1 = x_axis - 1
            y1 = y_axis
            pos_1 = (x1, y1)
            if pos_1 in flag_dict:
                if flag_dict[pos_1] == 0:
                    flag_dict[pos_1] = 1
                    list_x.append(x1)
                    list_y.append(y1)
                    append_x.append(x1)
                    append_y.append(y1)

            x2 = x_axis + 1
            y2 = y_axis
            pos_2 = (x2, y2)
            if pos_2 in flag_dict:
                if flag_dict[pos_2] == 0:
                    flag_dict[pos_2] = 1
                    list_x.append(x2)
                    list_y.append(y2)
                    append_x.append(x2)
                    append_y.append(y2)

            x3 = x_axis
            y3 = y_axis - 1
            pos_3 = (x3, y3)
            if pos_3 in flag_dict:
                if flag_dict[pos_3] == 0:
                    flag_dict[pos_3] = 1
                    list_x.append(x3)
                    list_y.append(y3)
                    append_x.append(x3)
                    append_y.append(y3)

            x4 = x_axis
            y4 = y_axis + 1
            pos_4 = (x4, y4)
            if pos_4 in flag_dict:
                if flag_dict[pos_4] == 0:
                    flag_dict[pos_4] = 1
                    list_x.append(x4)
                    list_y.append(y4)
                    append_x.append(x4)
                    append_y.append(y4)

        dist_x.append(append_x)
        dist_y.append(append_y)

    print("dist_x len: ", len(dist_x), len(dist_x[0]))
    print("dist_y len: ", len(dist_y), len(dist_y[0]))
    return dist_x, dist_y

# Generate depth of missing pixels
def generate_Depth(dist_x, dist_y, predicted_depth_mat, captured_depth_mat):

    dist_dict = []

    for i in range(len(dist_x)):

        cur_list_x = dist_x[i]
        cur_list_y = dist_y[i]
        cur_dict = {}

        for j in range(len(cur_list_x)):
            cur_x = cur_list_x[j]
            cur_y = cur_list_y[j]
            cur_pos = (cur_x, cur_y)
            cur_dict[cur_pos] = captured_depth_mat[cur_x][cur_y]

        dist_dict.append(cur_dict)

    gradient = calcGradient()

    nearby_pos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for i in range(1, len(dist_x)):
        cur_list_x = dist_x[i]
        cur_list_y = dist_y[i]

        for j in range(len(cur_list_x)):

            cur_x = cur_list_x[j]
            cur_y = cur_list_y[j]

            cur_depth_sum = 0
            count = 0

            for item in nearby_pos:
                near_x = cur_x + item[0]
                near_y = cur_y + item[1]

                if (near_x, near_y) in dist_dict[i-1]:
                    count += 1
                    cur_depth_sum += dist_dict[i-1][(near_x, near_y)] + gradient * (predicted_depth_mat[cur_x][cur_y] - predicted_depth_mat[near_x][near_y])

            cur_depth = cur_depth_sum / float(count)

            dist_dict[i][(cur_x, cur_y)] = cur_depth

    return dist_dict

if __name__ == "__main__":

    cur_dir = "./img/2796/"

    predicted_depth_filename = cur_dir + "depth.mat"
    captured_depth_filename = cur_dir + "distance.png"

    predicted_depth_mat = scipy.io.loadmat(predicted_depth_filename)
    predicted_depth_mat = predicted_depth_mat['x'][0]

    for i in range(len(predicted_depth_mat)):
        for j in range(len(predicted_depth_mat)):
            if predicted_depth_mat[i][j] == 1:
                predicted_depth_mat[i][j] = 1
            else:
                predicted_depth_mat[i][j] = 22 - predicted_depth_mat[i][j]

    print("predicted_depth_mat: ", predicted_depth_mat)

    captured_depth_mat = cv2.imread(captured_depth_filename, -1)
    for i in range(3):
        captured_depth_mat = ndimage.median_filter(captured_depth_mat, 10)

    print("captured_depth_mat: ", captured_depth_mat)

    dist_x, dist_y = calcDistance(predicted_depth_mat, captured_depth_mat)
    dist_dict = generate_Depth(dist_x, dist_y, predicted_depth_mat, captured_depth_mat)

    nobody_x, nobody_y = np.where(predicted_depth_mat == 1)
    for i in range(len(nobody_x)):
        captured_depth_mat[nobody_x[i]][nobody_y[i]] = 0

    for i in range(len(dist_dict)):
        for key in dist_dict[i].keys():
            cur_x = key[0]
            cur_y = key[1]
            captured_depth_mat[cur_x][cur_y] = dist_dict[i][key]

    refined_depth_mat = captured_depth_mat
    #refined_depth_mat = guidedfilter(predicted_depth_mat, captured_depth_mat, 40, 0.1)
    '''
    for key in dist_dict[0].keys():
        cur_x = key[0]
        cur_y = key[1]
        refined_depth_mat[cur_x][cur_y] = dist_dict[0][key]
    '''

    final_img = refined_depth_mat

    for i in range(len(final_img)):
        for j in range(len(final_img[0])):
            if final_img[i][j] < 0:
                final_img[i][j] = 0
            else:
                final_img[i][j] = final_img[i][j] * 20 / 256.0

    cv2.imwrite("res.jpg", final_img)