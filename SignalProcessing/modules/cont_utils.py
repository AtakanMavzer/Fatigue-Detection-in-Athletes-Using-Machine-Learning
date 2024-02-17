# Contraction utils

import pandas as pd
from features.time_features import *
from datetime import datetime
import pickle
import os
import json


# Basic sampen extractor
def to_sampen(L, m, r):
    N = len(L)
    B = 0.0
    A = 0.0
    # Split time series and save all templates of length m
    xmi = np.array([L[i: i + m] for i in range(N - m)])
    xmj = np.array([L[i: i + m] for i in range(N - m + 1)])
    # Save all matches minus the self-match, compute B
    B = np.sum([np.sum(np.abs(xmii - xmj).max(axis=1) <= r) - 1 for xmii in xmi])
    # Similar for computing A
    m += 1
    xm = np.array([L[i: i + m] for i in range(N - m + 1)])
    A = np.sum([np.sum(np.abs(xmi - xm).max(axis=1) <= r) - 1 for xmi in xm])

    # return sampen
    if np.isinf(-np.log(A / B)):
        print('inf detected')
        return np.nan
    else:
        return -np.log(A / B)

    # basic to frame


def to_frame(raw_data, frame_size, overlap):  # framelere bölme
    if overlap == 0:
        iter = int(raw_data.shape[0] / frame_size)
        frames = np.zeros([iter, frame_size])
        for k in range(iter):
            frames[k, :] = raw_data[((k) * frame_size):((k + 1) * frame_size)]
    else:
        iter = int(np.floor((raw_data.shape[0] - frame_size) / overlap + 1))
        frames = np.zeros([iter, frame_size])
        for k in range(iter):
            frames[k, :] = raw_data[((k) * overlap):((k) * overlap + frame_size)]
    return frames

def to_frame_divider(raw_data, frame_size, overlap):  # framelere bölme
    if overlap == 0:
        iter = int(len(raw_data) / frame_size)
        if iter < 0:
            return []
        frames = np.zeros([iter, frame_size])
        for k in range(iter):
            frames[k, :] = raw_data[((k) * frame_size):((k + 1) * frame_size)]
    else:
        iter = int(np.floor((len(raw_data) - frame_size) / overlap + 1))
        if iter < 0:
            return []
        frames = np.zeros([iter, frame_size])
        for k in range(iter):
            frames[k, :] = raw_data[((k) * overlap):((k) * overlap + frame_size)]
    return frames


def makeArray(text):
    text = text[1:-1]
    return np.fromstring(text, sep=',')


def find_index_of_digit(str):
    for i, c in enumerate(str):
        if c.isdigit():
            return i

def replaceWithMean(f):
    if np.isnan(f).any():
        mu = np.nanmean(f)
        ind = np.where(np.isnan(f))
        f[ind] = mu
    return f

def pklLoad(path_hist):
    print(path_hist)
    with open(path_hist, 'rb') as f:
        PKL = pickle.load(f)
    return PKL


def consecutiveRanges(a, n):
    length = 1
    list = []
    partition_count = 1
    partition = dict()
    # If the array is empty,
    # return the list
    if (n == 0):
        return list

    # Traverse the array
    # from first position
    for i in range(1, n + 1):

        # Check the difference
        # between the current
        # and the previous elements
        # If the difference doesn't
        # equal to 1 just increment
        # the length variable.
        if (i == n or a[i] -
                a[i - 1] != 1):

            # If the range contains
            # only one element.
            # add it into the list.
            if length == 1:
                list.append(str(a[i - length]))
            else:

                # Build the range between the first
                # element of the range and the
                # current previous element as the
                # last range.
                partition[str(partition_count)] = dict()
                partition[str(partition_count)]["start"] = a[i - length]
                partition[str(partition_count)]["stop"] = a[i - 1]
                partition_count += 1

                temp = (str(a[i - length]) +
                        " | " + str(a[i - 1]))
                list.append(temp)

            # After finding the 
            # first range initialize
            # the length by 1 to
            # build the next range.
            length = 1

        else:
            length += 1

    return partition


# if name_init 1, than cont_ muscle , muscle; o/w muscle , cont_muscle
def partioning(df, name_init):
    muscle = df.columns
    muscle_name = muscle[name_init::2]
    muscle_cont = muscle[int(1 - name_init)::2]

    partition = dict()

    i = 0
    for key in muscle_name:
        # partition[key] = dict()
        series = df.loc[df[muscle_cont[i]] == 1, muscle_cont[i]]
        # print("Muscle :" + key)
        # print( series )
        series = series.index
        part = consecutiveRanges(series.to_numpy(), len(series.to_numpy()))
        partition[key] = part

        i += 1

    return partition


def csv2pkl_neuro(player_name, team_name, filename, address):
    save_address = filename + "raw.pkl"
    df = []
    load_address = address + player_name + ".csv"
    # address + team_name + '/CSV/' + player_name + ".csv"
    df = pd.read_csv(load_address)
    df["data"] = df["data"].apply(makeArray).to_frame()
    timestamp = df.timeStamp[0] // 1000
    # time_str = time.ctime(timestamp)
    dt_object = str(datetime.fromtimestamp(timestamp))
    time_str = dt_object[:10]
    ab = df.sort_values(by=['timeStamp']).reset_index()
    min_time = ab['timeStamp'].iloc[0]
    max_time = ab['timeStamp'].iloc[-1]
    groupped = ab.groupby(["muscle_name"])
    segmented = pd.DataFrame(np.nan, index=range(max_time - min_time + 448),
                             columns=groupped.indices.keys())
    for index, row in ab.iterrows():
        diff = row['timeStamp'] - min_time
        segmented[row['muscle_name']][diff:diff + 448] = row['data']

        # file_path_creator(filename)
    segmented.to_pickle(save_address)
    print("saved successfully to  " + save_address)


# provide csv2pkl output as df
# epsilon : mean lower threashold
# time_threashold : interval
# mean_coef = mag threashold coef for mean
# sampen_co1 : m in sampen
# sampen_c2 : r in sampen    

# @return   df,contraction_dfs ( df: time x  16 ) 
# @return (contraction_dict : initial and end of cont as dict )
def contraction_detection(df, sampen_frame, sampen_overlap, time_threashold, epsilon, mean_coef, sampen_co1,
                          sampen_co2):
    # replace NaNs with mean
    for column in df.columns:
        df[column].fillna(value=df[column].mean(), inplace=True)

    # split columns
    dataframes = []

    for col in df.columns:
        dataframes.append(df[col])

    hist = dict()
    for x in dataframes:
        hist['sampen_' + x.name] = []

    # to_frame uygula
    i = 0
    for frame in dataframes:
        dataframes[i] = to_frame(frame, sampen_frame, sampen_overlap)
        i = i + 1

    # to_sampen uygula
    x = 0
    for key in hist:
        print(x)
        print(key)
        for k in dataframes[x]:
            if np.isnan(k).any():
                mu = np.nanmean(k);
                ind = np.where(np.isnan(k));
                k[ind] = mu

            hist[key] = np.append(hist[key], to_sampen(k, sampen_co1, sampen_co2))  # 3,0.02
        x = x + 1

    contraction_dfs = {}
    for muscle in hist:
        idxs = []
        arr = hist[muscle] > mean_coef * np.nanmean(hist[muscle])  # Magnitude threshold
        print("Mean for : " + muscle)
        print(np.nanmean(hist[muscle]))
        for i in range(len(arr) - time_threashold):
            if (arr[i:i + time_threashold].sum() > time_threashold - epsilon and arr[
                                                                                 i:i + time_threashold].sum() < time_threashold + epsilon):  # Duration threshold = 1900/32 = 60
                idxs.extend(range(i - 30, i + 70))  # Duration threshold +- 2

        idxs = np.array(idxs)
        # bool_arr = ( idxs < ( len(hist[muscle]) - int( sampen_frame / sampen_overlap) ) )
        idxs = idxs[(idxs < (len(hist[muscle]) - int(sampen_frame / sampen_overlap)))]
        idxs = list(idxs[idxs > 0])

        # idxs = list( idxs )

        contraction_times = np.array(idxs) * sampen_overlap + sampen_frame  #
        contraction_values = hist[muscle][idxs]  # contraction değerleri
        contraction_dfs[muscle] = pd.DataFrame(
            data={"time": contraction_times, "value": contraction_values})  # df'i oluştur

        columns = list(contraction_dfs.columns)
        inserted = columns.index(muscle)
        contraction_dfs.insert(inserted, "contractions_" + muscle, 0, allow_duplicates=False)

        time_stamp = contraction_dfs[muscle].time.values

        index_list = []
        print(len(time_stamp))
        for i in range(0, sampen_overlap):
            dummy = np.array(time_stamp)
            dummy = dummy + i
            index_list = np.append(index_list, dummy)

        unique_rows = np.unique(index_list, axis=0)
        unique_rows = unique_rows[unique_rows < len(df)]
        unique_rows = unique_rows.astype('int64')

        contraction_dfs.iloc[:, inserted][unique_rows] = 1

    contraction_dict = partioning(contraction_dfs, 1)

    return df, contraction_dict


# provide csv2pkl output as df
# provide sampen as hist dict for efficieny 
# epsilon : mean lower threashold
# time_threashold : interval
# mean_coef = mag threashold coef for mean
# sampen_co1 : m in sampen
# sampen_c2 : r in sampen    

# @return   df,contraction_dfs ( df: time x  16 ) 
# @return (contraction_dict : initial and end of cont as dict )
def contraction_detection_in_sampen(df, sampen_frame, sampen_overlap, time_threashold, epsilon, mean_coef, sampen_co1,
                                    sampen_co2):
    for column in df.columns:
        df[column].fillna(value=df[column].mean(), inplace=True)

    # split columns
    dataframes = []

    for col in df.columns:
        dataframes.append(df[col])

    hist = dict()
    for x in dataframes:
        hist[x.name] = []

    # to_frame uygula
    i = 0
    for frame in dataframes:
        dataframes[i] = to_frame(frame, sampen_frame, sampen_overlap)
        i = i + 1

    # to_sampen uygula
    x = 0
    for key in hist:
        print(x)
        print(key)
        for k in dataframes[x]:
            if np.isnan(k).any():
                mu = np.nanmean(k);
                ind = np.where(np.isnan(k));
                k[ind] = mu

            hist[key] = np.append(hist[key], to_sampen(k, sampen_co1, sampen_co2))  # 3,0.02
        x = x + 1

    contraction_dfs = {}
    for muscle in hist:
        idxs = []
        arr = hist[muscle] > mean_coef * np.nanmean(hist[muscle])  # Magnitude threshold
        print("Mean for : " + muscle)
        print(np.nanmean(hist[muscle]))
        for i in range(len(arr) - time_threashold):
            if (arr[i:i + time_threashold].sum() > time_threashold - epsilon and arr[
                                                                                 i:i + time_threashold].sum() < time_threashold + epsilon):  # Duration threshold = 1900/32 = 60
                idxs.extend(range(i - 30, i + 70))  # Duration threshold +- 2

        idxs = np.array(idxs)
        # bool_arr = ( idxs < ( len(hist[muscle]) - int( sampen_frame / sampen_overlap) ) )
        idxs = idxs[(idxs < (len(hist[muscle]) - int(sampen_frame / sampen_overlap)))]
        idxs = list(idxs[idxs > 0])

        # idxs = list( idxs )

        contraction_times = np.array(idxs) * sampen_overlap + sampen_frame  #
        contraction_values = hist[muscle][idxs]  # contraction değerleri
        contraction_dfs[muscle] = pd.DataFrame(
            data={"time": contraction_times, "value": contraction_values})  # df'i oluştur

        columns = list(df.columns)
        inserted = columns.index(muscle)
        df.insert(inserted, "contractions_" + muscle, 0, allow_duplicates=False)

        time_stamp = contraction_dfs[muscle].time.values

        index_list = []
        print(len(time_stamp))
        for i in range(0, sampen_overlap):
            dummy = np.array(time_stamp)
            dummy = dummy + i
            index_list = np.append(index_list, dummy)

        unique_rows = np.unique(index_list, axis=0)
        unique_rows = unique_rows[unique_rows < len(df)]
        unique_rows = unique_rows.astype('int64')

        df.iloc[:, inserted][unique_rows] = 1

    contraction_dict = partioning(df, 1)

    return df, contraction_dict


def csv_2_pkl_sync(df, save_address):
    # D:\Dönem Bitirme Projesi\SeniorProjectBucket\DATA\Team1\CSV\Subject1\training1_01_24_2021

    #match_data = os.path.dirname(os.path.realpath(__file__)) + "/"
    df["data"] = df["data"].apply(makeArray).to_frame()
    timestamp = df.timeStamp[0] // 1000
    dt_object = str(datetime.fromtimestamp(timestamp))
    time_str = dt_object[:10]

    ab = df.sort_values(by=['timeStamp']).reset_index()
    min_time = ab['timeStamp'].iloc[0]
    max_time = ab['timeStamp'].iloc[-1]
    groupped = ab.groupby(["muscle_name"])
    segmented = pd.DataFrame(np.nan, index=range(max_time - min_time + 448),
                             columns=groupped.indices.keys())

    for index, row in ab.iterrows():
        diff = row['timeStamp'] - min_time
        segmented[row['muscle_name']][diff:diff + 448] = row['data']
    print("save_address : " , save_address)
    if not os.path.exists(save_address):
        os.umask(0)
        os.makedirs(save_address)

    save_address += "/raw_data.pkl"
    segmented.to_pickle(save_address)
    print("saved successfully to " + save_address)
    """
    date = datetime.fromtimestamp(int(str(ab['timeStamp'][0])[:-3]))
    date = str(date)[:-9]
    with open("jsonFiles/matchdates.json") as json_file:
        match_dates = json.load(json_file)

    final_delta = -200
    tmp_delta = 0
    for idx , i in enumerate(match_dates):
        dt = pd.to_datetime(i, format='%Y/%m/%d')
        dt1 = pd.to_datetime(date, format='%Y/%m/%d')
        print("Bu dt -- " , dt)
        print("Bu dt1 -- " , dt1)
        delta = (dt1 - dt).days
        if delta >= -3 and delta <= 3:
            if abs(delta) < abs(tmp_delta):
                final_delta = delta

        tmp_delta = delta
    """
    return save_address
