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

        if(captured_depth_mat[y_pos][x_pos] != 0):
            captured_depth_nozeros.append(captured_depth_mat[y_pos][x_pos])

    captured_depth_nozeros_array = np.array(captured_depth_nozeros)
    mean_depth = np.mean(captured_depth_nozeros_array)
    min_depth = mean_depth - depth_range
    max_depth = mean_depth + depth_range
    print("captured raw human len: ", len(captured_depth_nozeros_array))
    print("min_depth: ", min_depth)
    print("max_depth: ", max_depth)

    captured_depth_x = []
    captured_depth_y = []

    for i in range(len(humanbody_x)):
        cur_x_pos = humanbody_x[i]
        cur_y_pos = humanbody_y[i]
        cur_depth = captured_depth_mat[cur_y_pos][cur_x_pos]

        if(cur_depth != 0 and cur_depth > min_depth and cur_depth < max_depth):
            captured_depth_x.append(cur_x_pos)
            captured_depth_y.append(cur_y_pos)

    print("captured depth len: ", len(captured_depth_x), len(captured_depth_y))

    return captured_depth_x, captured_depth_y

# Calculate pixels with different distance to captured data
def calcDistance(predicted_depth_mat, captured_depth_mat):

    humanbody_y, humanbody_x = np.where(predicted_depth_mat != 1)
    print("human pixel len: ", len(humanbody_x))

    captured_sample_y, captured_sample_x = np.where(captured_depth_mat != 0)
    print("captured sample len: ", len(captured_sample_x))

    captured_depth_x, captured_depth_y = removeOutliers(humanbody_x, humanbody_y, captured_depth_mat)

    captured_dict = {}
    for i in range(len(captured_depth_x)):
        cap_pos = (captured_depth_x[i], captured_depth_y[i])
        captured_dict[cap_pos] = captured_depth_mat[cap_pos[1]][cap_pos[0]]

    kernel_size = 4
    captured_nearby_pos = []
    for i in range(-1 * kernel_size, kernel_size + 1):
        for j in range(-1 * kernel_size, kernel_size + 1):
            item = (i, j)
            captured_nearby_pos.append(item)

    for key in captured_dict.keys():
        cur_x = key[0]
        cur_y = key[1]
        depth_val = 0
        count = 0
        for item in captured_nearby_pos:
            next_x = cur_x + item[0]
            next_y = cur_y + item[1]
            if (next_x, next_y) in captured_dict:
                count += 1
                depth_val += captured_depth_mat[next_y][next_x]

        captured_depth_mat[cur_y][cur_x] = depth_val / float(count)

    debug_mat_2 = np.zeros_like(captured_depth_mat)
    for i in range(len(captured_depth_x)):
        debug_mat_2[captured_depth_y[i]][captured_depth_x[i]] = captured_depth_mat[captured_depth_y[i]][captured_depth_x[i]]
    debug_mat_2 = debug_mat_2 * 20.0 / 256.0
    cv2.imwrite("debug 2.jpg", debug_mat_2)

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

    nearby_pos = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, +1), (+1, -1), (+1, +1)]
    #nearby_pos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while len(list_x) != len(humanbody_x):
        cur_list_x = dist_x[-1]
        cur_list_y = dist_y[-1]

        append_x = []
        append_y = []

        for i in range(len(cur_list_x)):

            x_axis = cur_list_x[i]
            y_axis = cur_list_y[i]

            for item in nearby_pos:
                next_x = x_axis + item[0]
                next_y = y_axis + item[1]
                next_pos = (next_x, next_y)

                if next_pos in flag_dict:
                    if flag_dict[next_pos] == 0:
                        flag_dict[next_pos] = 1
                        list_x.append(next_x)
                        list_y.append(next_y)
                        append_x.append(next_x)
                        append_y.append(next_y)

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
            cur_dict[cur_pos] = captured_depth_mat[cur_y][cur_x]

        dist_dict.append(cur_dict)

    reserved_dict = copy.deepcopy(dist_dict[0])

    gradient = calcGradient()

    nearby_pos = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, +1), (+1, -1), (+1, +1), (-2, -2), (-2, -1),
                  (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, +2), (0, -2), (0, +2), (+1, -2), (+1, +2), (+2, -2),
                  (+2, -1), (+2, 0), (+2, +1), (+2, +2)]

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

                if (near_x, near_y) in reserved_dict:
                    count += 1
                    cur_depth_sum += reserved_dict[(near_x, near_y)] + gradient * (predicted_depth_mat[cur_y][cur_x] - predicted_depth_mat[near_y][near_x])

            cur_depth = cur_depth_sum / float(count)

            dist_dict[i][(cur_x, cur_y)] = cur_depth
            reserved_dict[(cur_x, cur_y)] = cur_depth

    return dist_dict

if __name__ == "__main__":

    cur_dir = "./img/2796/"
    predicted_depth_filename = cur_dir + "depth.mat"
    captured_depth_filename = cur_dir + "distance.png"

    predicted_depth_mat = scipy.io.loadmat(predicted_depth_filename)
    predicted_depth_mat = predicted_depth_mat['x'][0]
    print("predicted_depth_mat: ", predicted_depth_mat)

    captured_depth_mat = cv2.imread(captured_depth_filename, -1)
    for i in range(3):
        captured_depth_mat = ndimage.median_filter(captured_depth_mat, 10)

    debug_mat_1 = copy.deepcopy(captured_depth_mat)
    debug_mat_1 = debug_mat_1 * 20.0 / 256.0
    cv2.imwrite("debug 1.jpg", debug_mat_1)

    dist_x, dist_y = calcDistance(predicted_depth_mat, captured_depth_mat)
    dist_dict = generate_Depth(dist_x, dist_y, predicted_depth_mat, captured_depth_mat)

    nobody_y, nobody_x = np.where(predicted_depth_mat == 1)
    for i in range(len(nobody_x)):
        captured_depth_mat[nobody_y[i]][nobody_x[i]] = 0

    for i in range(len(dist_dict)):
        for key in dist_dict[i].keys():
            cur_x = key[0]
            cur_y = key[1]
            captured_depth_mat[cur_y][cur_x] = dist_dict[i][key]

    #refined_depth_mat = copy.deepcopy(captured_depth_mat)
    refined_depth_mat = guidedfilter(predicted_depth_mat, captured_depth_mat, 40, 0.1)

    '''
    for key in dist_dict[0].keys():
        cur_x = key[0]
        cur_y = key[1]
        refined_depth_mat[cur_y][cur_x] = dist_dict[0][key]
    '''

    final_img = copy.deepcopy(refined_depth_mat)

    for i in range(len(final_img)):
        for j in range(len(final_img[0])):
            if final_img[i][j] <= 0:
                final_img[i][j] = 0
            else:
                final_img[i][j] = final_img[i][j] * 20 / 256.0


    save_name = "res_" + cur_dir[-5:-1] + ".jpg"
    cv2.imwrite(save_name, final_img)

    show_mat = cv2.imread(save_name, 0)
    cv2.imshow("show", show_mat)
    cv2.waitKey()