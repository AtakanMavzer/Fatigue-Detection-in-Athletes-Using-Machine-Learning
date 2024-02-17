import numpy as np
import pandas as pd
import numpy
from modules.cont_utils import *
from features.time_features import *
from features.freq_features import *
import statistics
import sys

try:
    constants = json.load(open("math_constant/constants.json"))
except:
    print("Math Constants Does not exist please fix")


def feature_engineering(muscle_array, df, partition, size, overlap):

    feature_dict_array = []
    index_count = 0
    while len(muscle_array) > index_count:
        splitted_muscle = muscle_array[index_count].split(" ")
        main_muscle_name = splitted_muscle[0] + " " + splitted_muscle[1]

        right_side_muscle = main_muscle_name + " " + "Right"
        left_side_muscle = main_muscle_name + " " + "Left"

        if len(partition[right_side_muscle]) >= len(partition[left_side_muscle]) and \
                len(partition[right_side_muscle]) != 0:
            for x in range(1, len(partition[right_side_muscle]) + 1):
                start_x = partition[right_side_muscle][str(x)]['start']
                end_x = partition[right_side_muscle][str(x)]['stop']

                to_frame_2d_array_right, to_frame_2d_array_left = frame_calculator(main_muscle_name,
                                                                                   df,
                                                                                   start_x,
                                                                                   end_x)
                if "linear" in constants["timezone_type"]:
                    BL_MNF_right_row_array = BandlimitMNF_calculator(to_frame_2d_array_right, size, overlap)
                    BL_MNF_left_row_array = BandlimitMNF_calculator(to_frame_2d_array_left, size, overlap)
                    RMS_right_row_array = RMS_calculator(to_frame_2d_array_right, size, overlap)
                    RMS_left_row_array = RMS_calculator(to_frame_2d_array_left, size, overlap)
                    MNF_right_row_array = MNF_calculator(to_frame_2d_array_right, size, overlap)
                    MNF_left_row_array = MNF_calculator(to_frame_2d_array_left, size, overlap)

                EMG_divided_array_right, EMG_divided_array_left = size_calculator(right_side_muscle, size,
                                                                                  to_frame_2d_array_right,
                                                                                  to_frame_2d_array_left)
                for index in range(0, len(MNF_right_row_array)):
                    each_muscle_feature_dict = {}
                    if len(EMG_divided_array_right) <= index:
                        each_muscle_feature_dict["R"] = EMG_divided_array_right[len(EMG_divided_array_right) - 1]
                    else:
                        each_muscle_feature_dict["R"] = EMG_divided_array_right[index]
                    each_muscle_feature_dict["R_MNF"] = MNF_right_row_array[index]
                    each_muscle_feature_dict["R_RMS"] = RMS_right_row_array[index]
                    for row_count in range(1, len(BL_MNF_right_row_array) + 1):
                        each_muscle_feature_dict["R_BL_MNF_" + str(row_count)] = BL_MNF_right_row_array[str(row_count)][
                            index]
                    if len(EMG_divided_array_left) <= index:
                        each_muscle_feature_dict["L"] = EMG_divided_array_left[len(EMG_divided_array_left) - 1]
                    else:
                        each_muscle_feature_dict["L"] = EMG_divided_array_left[index]
                    each_muscle_feature_dict["L_MNF"] = MNF_left_row_array[index]
                    each_muscle_feature_dict["L_RMS"] = RMS_left_row_array[index]
                    for row_count in range(1, len(BL_MNF_left_row_array) + 1):
                        each_muscle_feature_dict["L_BL_MNF_" + str(row_count)] = BL_MNF_left_row_array[str(row_count)][
                            index]
                    each_muscle_feature_dict["muscle"] = main_muscle_name
                    each_muscle_feature_dict["partition"] = x
                    each_muscle_feature_dict["total_partition"] = len(partition[right_side_muscle])
                    feature_dict_array.append(each_muscle_feature_dict)
            index_count += 2
        elif len(partition[left_side_muscle]) > len(partition[right_side_muscle]) and \
                len(partition[left_side_muscle]) != 0:
            for x in range(1, len(partition[left_side_muscle]) + 1):
                start_x = partition[left_side_muscle][str(x)]['start']
                end_x = partition[left_side_muscle][str(x)]['stop']

                to_frame_2d_array_right, to_frame_2d_array_left = frame_calculator(main_muscle_name,
                                                                                   df,
                                                                                   start_x,
                                                                                   end_x)
                if "linear" in constants["timezone_type"]:
                    BL_MNF_right_row_array = BandlimitMNF_calculator(to_frame_2d_array_right, size, overlap)
                    BL_MNF_left_row_array = BandlimitMNF_calculator (to_frame_2d_array_left, size, overlap)
                    RMS_right_row_array = RMS_calculator(to_frame_2d_array_right, size, overlap)
                    RMS_left_row_array = RMS_calculator(to_frame_2d_array_left, size, overlap)
                    MNF_right_row_array = MNF_calculator(to_frame_2d_array_right, size, overlap)
                    MNF_left_row_array = MNF_calculator(to_frame_2d_array_left, size, overlap)

                EMG_divided_array_right, EMG_divided_array_left = size_calculator(left_side_muscle, size,
                                                                                  to_frame_2d_array_right,
                                                                                  to_frame_2d_array_left)
                for index in range(0, len(MNF_left_row_array)):
                    each_muscle_feature_dict = {}
                    each_muscle_feature_dict["R"] = EMG_divided_array_right[index]
                    each_muscle_feature_dict["R_MNF"] = MNF_right_row_array[index]
                    each_muscle_feature_dict["R_RMS"] = RMS_right_row_array[index]
                    each_muscle_feature_dict["R_BL_MNF"] = BL_MNF_right_row_array[index]
                    each_muscle_feature_dict["L"] = EMG_divided_array_right[index]
                    each_muscle_feature_dict["L_MNF"] = MNF_left_row_array[index]
                    each_muscle_feature_dict["L_RMS"] = RMS_left_row_array[index]
                    each_muscle_feature_dict["L_BL_MNF"] = BL_MNF_left_row_array[index]
                    each_muscle_feature_dict["muscle"] = main_muscle_name
                    each_muscle_feature_dict["partition"] = x
                    each_muscle_feature_dict["total_partition"] = len(partition[right_side_muscle])
                    feature_dict_array.append(each_muscle_feature_dict)
            index_count += 2

        else:
            print("This Muscle doesn't have any partition : ", main_muscle_name)
            each_muscle_feature_dict = {}
            each_muscle_feature_dict["R"] = []
            each_muscle_feature_dict["R_MNF"] = []
            each_muscle_feature_dict["R_RMS"] = []
            each_muscle_feature_dict["R_BL_MNF"] = []
            each_muscle_feature_dict["L"] = []
            each_muscle_feature_dict["L_MNF"] = []
            each_muscle_feature_dict["L_RMS"] = []
            each_muscle_feature_dict["L_BL_MNF"] = []
            each_muscle_feature_dict["muscle"] = main_muscle_name
            each_muscle_feature_dict["partition"] = 0
            each_muscle_feature_dict["total_partition"] = 0
            feature_dict_array.append(each_muscle_feature_dict)
            index_count += 2
    return feature_dict_array

def label_extractor(df,contraction_list ,size, overlap):
    feature_dict_array = []
    for index in range(1, len(contraction_list) + 1):
        for count, row in df.iterrows():
            if count + 1 == index:
                try:
                    label_muscle_list = contraction_list[str(index)][row["label"]]
                except:
                    print("ERROR during taking label " + row["label"])
                for label_muscle in label_muscle_list:
                    if label_muscle == "X":
                        print("Label ignore detected, system continues"
                              "")
                        continue
                    elif label_muscle == "BF":
                        main_muscle_name = "Biceps Femoris"
                        feature_dict_array = feature_dict_array + (feature_engineering_v2(main_muscle_name,
                                                                                          row,
                                                                                          size,
                                                                                          row["label"],
                                                                                          index,
                                                                                          len(contraction_list),
                                                                                          overlap))
                    elif label_muscle == "CI":
                        main_muscle_name = "Calves Inner"
                        feature_dict_array = feature_dict_array + (feature_engineering_v2(main_muscle_name,
                                                                                          row,
                                                                                          size,
                                                                                          row["label"],
                                                                                          index,
                                                                                          len(contraction_list),
                                                                                          overlap))
                    elif label_muscle == "RF":
                        main_muscle_name = "Rectus Femoris"
                        feature_dict_array = feature_dict_array + (feature_engineering_v2(main_muscle_name,
                                                                                          row,
                                                                                          size,
                                                                                          row["label"],
                                                                                          index,
                                                                                          len(contraction_list),
                                                                                          overlap))
                    elif label_muscle == "AL":
                        main_muscle_name = "Adductor Longus"
                        feature_dict_array = feature_dict_array + (feature_engineering_v2(main_muscle_name,
                                                                         row,
                                                                         size,
                                                                         row["label"],
                                                                         index,
                                                                         len(contraction_list),
                                                                         overlap))
    return feature_dict_array

def feature_engineering_v2(main_muscle_name,row,size,label_name, contraction_count, total_contraction, overlap):
    frame_mean_dict = {}
    local_feature_dict_array = []
    graph_dict = {}
    right_side_muscle = main_muscle_name + " " + "Right"
    left_side_muscle = main_muscle_name + " " + "Left"
    to_frame_2d_array_right, to_frame_2d_array_left = frame_calculator(main_muscle_name, row, 0, 0)
    if "linear" in constants["timezone_type"]:
        BL_MNF_right_row_array = BandlimitMNF_calculator(to_frame_2d_array_right, size, overlap)
        BL_MNF_left_row_array = BandlimitMNF_calculator(to_frame_2d_array_left, size, overlap)
        RMS_right_row_array = RMS_calculator(to_frame_2d_array_right, size, overlap)
        RMS_left_row_array = RMS_calculator(to_frame_2d_array_left, size, overlap)
        MNF_right_row_array = MNF_calculator(to_frame_2d_array_right, size, overlap)
        MNF_left_row_array = MNF_calculator(to_frame_2d_array_left, size, overlap)

    EMG_divided_array_right, EMG_divided_array_left = size_calculator(right_side_muscle, size,
                                                                      to_frame_2d_array_right,
                                                                      to_frame_2d_array_left)
    for index in range(0, len(MNF_right_row_array)):
        each_muscle_feature_dict = {}
        if len(EMG_divided_array_right) <= index:
            each_muscle_feature_dict["R"] = EMG_divided_array_right[len(EMG_divided_array_right)-1]
        else:
            each_muscle_feature_dict["R"] = EMG_divided_array_right[index]
        each_muscle_feature_dict["R_MNF"] = MNF_right_row_array[index]
        each_muscle_feature_dict["R_RMS"] = RMS_right_row_array[index]
        for row_count in range(1,len(BL_MNF_right_row_array) + 1):
            each_muscle_feature_dict["R_BL_MNF_"+str(row_count)] = BL_MNF_right_row_array[str(row_count)][index]
        if len(EMG_divided_array_left) <= index:
            each_muscle_feature_dict["L"] = EMG_divided_array_left[len(EMG_divided_array_left) - 1]
        else:
            each_muscle_feature_dict["L"] = EMG_divided_array_left[index]
        each_muscle_feature_dict["L_MNF"] = MNF_left_row_array[index]
        each_muscle_feature_dict["L_RMS"] = RMS_left_row_array[index]
        for row_count in range(1,len(BL_MNF_left_row_array) + 1):
            each_muscle_feature_dict["L_BL_MNF_"+str(row_count)] = BL_MNF_left_row_array[str(row_count)][index]
        each_muscle_feature_dict["muscle"] = main_muscle_name
        each_muscle_feature_dict["label"] = label_name
        each_muscle_feature_dict["partition"] = contraction_count
        each_muscle_feature_dict["total_partition"] = total_contraction
        local_feature_dict_array.append(each_muscle_feature_dict)

    return local_feature_dict_array


def frame_calculator(muscle_name,df,start_x, end_x):
    if start_x == 0 and end_x == 0:
        right_side_muscle = muscle_name + " " + "Right"
        left_side_muscle = muscle_name + " " + "Left"
        tmp_right_array = df[right_side_muscle].to_numpy()
        tmp_left_array = df[left_side_muscle].to_numpy()
    else:
        tmp_right = df[start_x: end_x][muscle_name + " " + "Right"]
        tmp_left = df[start_x: end_x][muscle_name + " " + "Left"]
        tmp_right_array = tmp_right.to_numpy()
        tmp_left_array = tmp_left.to_numpy()

    to_frame_2d_array_right = to_frame(tmp_right_array, constants["sampen_frame"], constants["sampen_overlap"])
    to_frame_2d_array_left = to_frame(tmp_left_array, constants["sampen_frame"], constants["sampen_overlap"])
    delete_array = []
    for index,row in enumerate(to_frame_2d_array_right):
        mean_value_right = np.nanmean(to_frame_2d_array_right[index])
        mean_value_left = np.nanmean(to_frame_2d_array_left[index])
        if np.isnan(mean_value_right) or np.isnan(mean_value_left):
            delete_array.append(index)
    to_frame_2d_array_right = np.delete(to_frame_2d_array_right, delete_array, axis = 0)
    to_frame_2d_array_left = np.delete(to_frame_2d_array_left, delete_array, axis = 0)

    delete_array = []

    for index,row in enumerate(to_frame_2d_array_right):
        to_frame_2d_array_right[index] = replaceWithMean(to_frame_2d_array_right[index])
        to_frame_2d_array_left[index] = replaceWithMean(to_frame_2d_array_left[index])
        if same_array_finder(to_frame_2d_array_right[index]) or same_array_finder(to_frame_2d_array_left[index]):
            delete_array.append(index)
    to_frame_2d_array_right = np.delete(to_frame_2d_array_right, delete_array, axis = 0)
    to_frame_2d_array_left = np.delete(to_frame_2d_array_left, delete_array, axis = 0)
    return to_frame_2d_array_right, to_frame_2d_array_left

def size_calculator(selected_muscle_name, size, frame_2d_array_left, frame_2d_array_right):

    if "Left" in selected_muscle_name:
        tmp_frame_length_count = int(len(frame_2d_array_left) / size)
    elif "Right" in selected_muscle_name:
        tmp_frame_length_count = int(len(frame_2d_array_left) / size)
    else:
        print("There is a mistake in size calculation please check")
        tmp_frame_length_count = 0

    tmp_divided_arrays_right = []
    tmp_divided_arrays_left = []
    for index in range(0, tmp_frame_length_count):
        tmp_divided_flatten_right = frame_2d_array_right[(index * size) :
                                                         ((index + 1 ) * size)].flatten()
        tmp_divided_arrays_right.append(tmp_divided_flatten_right)

        tmp_divided_flatten_left = frame_2d_array_left[(index * size) :
                                                       ((index + 1 ) * size)].flatten()
        tmp_divided_arrays_left.append(tmp_divided_flatten_left)

    return tmp_divided_arrays_right, tmp_divided_arrays_left

def MNF_calculator(frame_array , size, overlap):
    MNF_array = []
    for count,y in enumerate(frame_array):
        MNF_array.append(to_MNF(y))
    MNF_array_row = to_frame_divider(MNF_array, size, overlap)
    return MNF_array_row

def RMS_calculator(frame_array , size, overlap):
    RMS_array = []
    for count,y in enumerate(frame_array):
        RMS_array.append(to_RMS(y))
    RMS_array_row = to_frame_divider(RMS_array, size, overlap)
    return RMS_array_row

def BandlimitMNF_calculator(frame_array, size, overlap):
    BL_MNF_array = []
    BL_MNF_seperated_dict = {}
    for index in range(1,len(constants["bandLimitDict"]) + 1):
        BL_MNF_seperated_dict[str(index)] = []
    for count,y in enumerate(frame_array):
        rawEMGPowerSpectrum, frequencies = to_updatedPSD(y)
        taken_splitted_dict = splitFreqBandLimit(rawEMGPowerSpectrum,
                                                     frequencies,
                                                     constants["bandLimitDict"])

        for index in range(0,len(constants["bandLimitDict"])):
            #BL_MNF_array.append(to_BL_MNF(taken_splitted_dict[index]["emgPS"],
                                          #taken_splitted_dict[index]["freq"]))
            BL_MNF_seperated_dict[str(index+1)].append(to_BL_MNF(taken_splitted_dict[index]["emgPS"],
                                                                 taken_splitted_dict[index]["freq"]))
    #BL_MNF_row_array = to_frame_divider(BL_MNF_array,size*len(constants["bandLimitDict"]),0)
    for index in range(1,len(constants["bandLimitDict"]) + 1):
        BL_MNF_seperated_dict[str(index)] = to_frame_divider(BL_MNF_seperated_dict[str(index)],size,overlap)
    return BL_MNF_seperated_dict


def double_nan_checker(frame_array):
    frame_nan_array = []
    for y in frame_array:
        frame_nan_array.append(np.mean(y))
    for count,y in enumerate(frame_array):
        y = replaceWithMean(y)
        if np.isnan(y).any():
            if count == 0:
                counter = count
                while True:
                    counter = counter + 1
                    if np.isnan(frame_nan_array[counter]):
                        continue
                    else:
                        y[:] = frame_nan_array[counter]
                        if np.isnan(y).any():
                            print("Somethings wrong")
                            print(frame_nan_array[counter])
                        break
            else:
                counter = count
                while counter > -1:
                    counter = counter - 1
                    if np.isnan(frame_nan_array[counter]):
                        continue
                    else:
                        y[:] = frame_nan_array[counter]
                        if np.isnan(y).any():
                            print("Somethings wrong")
                            print(frame_nan_array[counter])
    return frame_array

def same_array_finder(array):
    tmp = array[0]
    for index in range(1,len(array)):
        if not array[index] == tmp and not np.isnan(array[index]):
            return False
    return True