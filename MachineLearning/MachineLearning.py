from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers import LSTM
from keras.models import Model
from sklearn.linear_model import LinearRegression
from keras.layers import Bidirectional
import pandas as pd
import numpy as np
import tensorflow as tf
import seaborn as snNew
from datetime import datetime as dt
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import json
from send_data import *


file = open(r"../DATA/PKL/Team1/merged/all_merged_featured.pkl", "rb")

dataset = pd.read_pickle(file)

dataset = dataset[dataset['match_day'] > -20]

with open(r"final_player_stat.json", "rb") as f:
    data = json.load(f)

dataset['fatigue'] = ""
subject_list_df = []
for count, row in dataset.iterrows():
    timestamp = dt.strptime(row['timestamp'], '%Y-%m-%d')
    timestamp = str(timestamp)[:-9]
    name = row['subject']
    subject_list_df.append({"subject" : row['subject'] , 'date':row['timestamp']})
    for i in data:
        if i['name'] == name and i['date'] == timestamp:
            dataset.loc[count, 'fatigue'] = i['fatigue'][1]

match_days = dataset['match_day']


def findMax(arr):
    maxElement = np.amax(arr)
    return maxElement


def findMinimum(arr):
    minElement = np.min(arr)
    return minElement


df_normalized = pd.DataFrame.from_dict(dataset)
temp = []

double_temp = [[], []]


def normalizeMyData():
    for count, row in df_normalized.iterrows():
        new_dict = {}
        for index, column in enumerate(df_normalized.columns):

            if index < 12:
                min = findMinimum(row[column])
                max = findMax(row[column])
                new_dict[column] = ((row[column] - min) / (max - min)) * 10

        temp.append(new_dict)

    df = pd.DataFrame(temp)

    return df


normalized_dataset = normalizeMyData()

normalized_dataset["fatigue"] = dataset['fatigue'].values


def fatigue_json_calculator(subject_array, date_array):
    with open(r"C:\Users\User\Desktop\CMPE491\final_player_stat.json", "rb") as f:
        data = json.load(f)
    fatigue_json_array = []
    for count in range(0, len(subject_array)):
        for i in data:
            if i["name"] == subject_array[count] and i["date"] == date_array[count]:
                fatigue_json_array.append(i["fatigue"][1])

    fatigue_np_array = np.array(fatigue_json_array)
    return fatigue_np_array


encoded = dataset['match_day']
encoded = list(encoded)


onehot_encoder = OneHotEncoder(sparse = False)
reshaped = np.array(encoded).reshape(len(encoded), 1)
onehot = onehot_encoder.fit_transform(reshaped)
reverseOneHot = onehot_encoder.inverse_transform(onehot)


def forward_pass(y_pred, y_test):
    # Converting predictions to label
    pred = list()
    for i in range(len(y_pred)):
        pred.append(np.argmax(y_pred[i]))

    # Converting one hot encoded test label to label
    test = list()
    for i in range(len(y_test)):
        test.append(np.argmax(y_test[i]))

    print("=== Test Set Performance ===")
    a = accuracy_score(pred, test)
    print('Accuracy is:', a * 100)

    f1 = f1_score(pred, test, average = 'weighted')
    f1_class = f1_score(test, pred, average = None)
    print('f1: ', f1 * 100)
    print("F1 class based:")
    print(f1_class)

    y_pred = np.argmax(y_pred, axis = 1)
    y_test = np.argmax(y_test, axis = 1)

    c_m = confusion_matrix(y_test, y_pred)
    snNew.heatmap(c_m, annot = True)

    return c_m



selective_feature = ["R_MNF", "R_RMS", "L_MNF", "L_RMS", "R_BL_MNF_1", "L_BL_MNF_1", "fatigue"]

selective_feature_1 = ["R_MNF", "R_RMS", "L_MNF", "L_RMS"]
selective_feature_2 = ["R_BL_MNF_1", "L_BL_MNF_1"]
selective_feature_3 = ["R_BL_MNF_2", "L_BL_MNF_2"]
selective_feature_4 = ["R_BL_MNF_3", "L_BL_MNF_3"]

output_number = len(dataset['match_day'].unique())

userInput = "1"
model = Sequential()
if (userInput == "0"):
    model.add(LSTM(16, activation = 'relu', input_shape = (61, 6), return_sequences = False))

elif (userInput == "1"):
    model.add(Bidirectional(LSTM(32, activation = 'relu', input_shape = (61, 6), return_sequences = False)))

model.add(Dense(16, activation = 'tanh'))

model.add(Dense(8, activation = 'tanh'))

model.add(Dense(output_number, activation = 'softmax'))

model.compile(optimizer = "adam", loss = "categorical_crossentropy", metrics = ["accuracy"])

checkpoint = [
    tf.keras.callbacks.ModelCheckpoint(
        'trial_ml001' + 'model{epoch:02d}.h5', save_freq = 1
    )
]


X_train = np.zeros((len(normalized_dataset), 61, len(selective_feature)))  ###ESKİSİ
y_train = np.array(onehot)

X_trainA = np.zeros((len(normalized_dataset), 61, len(selective_feature)))
y_trainA = np.array(reverseOneHot)



userInput = "1"
counter = -1
if userInput == "0":
    print("******")
    for x in selective_feature_1:
        counter = counter + 1
        for i in range(0, len(normalized_dataset)):
            X_train[i, :, counter] = normalized_dataset.iloc[i][x]

if userInput == "1":
    new_array_count_1 = selective_feature_1 + selective_feature_2
    for x in new_array_count_1:
        counter = counter + 1

        for i in range(0, len(normalized_dataset)):
            X_train[i, :, counter] = normalized_dataset.iloc[i][x]

    for i in range(0, len(normalized_dataset)):
        #fatigue_array[i,:,0] = [normalized_dataset.iloc[i]['fatigue']] * 61
        X_train[i, :, 6] = [normalized_dataset.iloc[i]['fatigue']] * 61

if userInput == "2":
    new_array_count_2 = selective_feature_1 + selective_feature_3
    for x in new_array_count_2:
        counter = counter + 1
        for i in range(0, len(normalized_dataset)):
            X_train[i, :, counter] = normalized_dataset.iloc[i][x]

if userInput == "3":
    new_array_count_3 = selective_feature_1 + selective_feature_4
    for x in new_array_count_3:
        counter = counter + 1
        for i in range(0, len(normalized_dataset)):
            X_train[i, :, counter] = normalized_dataset.iloc[i][x]

if userInput == "4":
    new_array_count_4 = selective_feature_1 + selective_feature_2 + selective_feature_3 + selective_feature_4
    for x in new_array_count_4:
        counter = counter + 1
        for i in range(0, len(normalized_dataset)):
            X_train[i, :, counter] = normalized_dataset.iloc[i][x]

target_date = dataset["timestamp"].iloc[-1]
target_subject = dataset["subject"].iloc[-1]
target_subject_id = dataset["subject_id"].iloc[-1]
start_x = -1
end_x = len(dataset)
for count , elements in enumerate(subject_list_df):
    if elements["date"] == target_date and elements["subject"] == target_subject:
        if start_x == -1:
            start_x = count
            break
X_target = X_train[start_x : end_x]
y_target = y_train[start_x : end_x]
X_train = np.delete(X_train, np.s_[start_x:end_x], axis=1)
y_train = np.delete(y_train, np.s_[start_x:end_x], axis=1)

fatigue_array = X_train[:,:,6]
fatigue_test_array = X_target[:,:,6]

history = model.fit(X_train, y_train, epochs = 1, verbose = 1, shuffle = True, callbacks = checkpoint,
                    validation_split = 0.2)

model.summary()

y_prediction = model.predict(X_target)
forward_pass(y_prediction, y_target)

"""
metric = "accuracy"
plt.figure()
plt.plot(history.history[metric])
plt.plot(history.history["val_" + metric])
plt.title("model " + metric)
plt.ylabel(metric, fontsize = "large")
plt.xlabel("epoch", fontsize = "large")
plt.legend(["train", "val"], loc = "best")
plt.show()
plt.close()
"""


reduced_model = Model(inputs = model.input, outputs = model.get_layer("dense_1").output)
feature_vector_train = reduced_model.predict(X_train)
train_featureVector_yTrain = np.column_stack((feature_vector_train, fatigue_array[:,1]))
X_train = train_featureVector_yTrain[:,0:7]
Y_train = train_featureVector_yTrain[:,8]


feature_vector_test_train = reduced_model.predict(X_target)
train_featureVector_test_yTrain = np.column_stack((feature_vector_test_train, fatigue_test_array[:,1]))

X_train_test = train_featureVector_test_yTrain[:,0:7]
Y_train_test = train_featureVector_test_yTrain[:,8]


model = LinearRegression().fit(X_train, Y_train)
r_sq = model.score(X_train, Y_train)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)



test_model = model.predict(X_train_test)
print(test_model)

calculated_fatigue_result = sum(test_model) / len(test_model)

print("Fatigue Result : " ,calculated_fatigue_result)

send_data(target_subject_id , target_date, calculated_fatigue_result)
