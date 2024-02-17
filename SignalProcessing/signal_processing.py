from re import S
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import os
import time
import errno
import pickle
import json
from datetime import datetime
from pathlib import Path
import math
from modules.cont_utils import *
from helpers.helpers import *
from modules.feature_engineering import *
from features.freq_features import *
from features.time_features import *
import statistics


class signal_processing_pkl_v2:
    def __init__(self, data_address, bucket_save_address, test_mode):
        try:
            self.db_player_list = json.load(open("jsonFiles/subject_database.json"))
        except:
            print("subject_database.json does not exists please check")
        self.data_address = data_address
        self.bucket_save_address = bucket_save_address
        self.test_mode = test_mode

        # Taking Math constants
        try:
            self.constants = json.load(open("math_constant/constants.json"))
        except:
            print("Math Constants Does not exist please fix")

        # Taking Contraction info
        try:
            self.contractions = json.load(open("jsonFiles/training_player_info.json"))
        except:
            print("training_player_info.json does not exist please check")
        # These variables are taking their values in data_selector()
        self.player_id = ""
        self.player_name = ""
        self.training_folder_name = ""
        self.training_time = ""
        self.match_day = ""
        self.raw_training_file_path = ""

        # These variables are taking their values in file_creating()
        self.subject_name = ""
        self.target_training_folder_path = ""
        self.target_training_file_path = ""
        self.target_aws_training_file_path = ""

        # These variables are taking their values in partition_finder()
        self.muscle_array = []
        self.df = ""
        self.contraction_list = {}

        # These variables are taking their values in signal_processing()
        self.created_df = ""

    def data_selector(self):
        print("Calculation is starting ...")
        time.sleep(2)
        data_files = os.listdir(self.data_address)
        for file in data_files:
            training_file_path = self.data_address + "/" + file
            self.player_name = file
            print(self.player_name)
            self.player_id = player_id_founder(file, self.db_player_list)
            if self.player_id == "":
                continue
            training_files = os.listdir(training_file_path)
            for training in training_files:
                self.training_folder_name = training
                tmp_name = self.training_folder_name.split("__")
                # tmp_name[0] = training1 , training2 etc.
                # tmp_name[1] = date of training 2022-01-10 , 2021-12-02 etc.
                self.training_time = tmp_name[1]
                self.match_day = match_day_calculator(self.training_time)
                self.match_frequency = match_frequency_counter(self.training_time)
                self.raw_training_file_path = training_file_path + "/" + training + "/labeled.pkl"
                self.signal_processing()
        return

    def file_creating(self):
        self.subject_name = subject_db_checker(self.player_id)
        print("Subject Name " + self.subject_name)
        target_subject_folder = self.bucket_save_address + "/" + self.subject_name
        if not os.path.exists(target_subject_folder):
            os.umask(0)
            os.makedirs(target_subject_folder)
        target_training_folder = target_subject_folder + "/" + self.training_folder_name
        if not os.path.exists(target_training_folder):
            os.umask(0)
            os.makedirs(target_training_folder)
        self.target_training_folder_path = target_training_folder
        self.target_training_file_path = self.target_training_folder_path + "/featured.pkl"

    def partition_finder(self):
        with open(self.raw_training_file_path, 'rb') as file:
            self.df = pickle.load(file)

        muscles = self.df.columns
        self.muscle_array = muscles[:-2]

        self.contraction_list = self.contractions[self.player_name][self.training_time]
    def signal_processing(self):
        # Creating training folder in bucket
        self.file_creating()

        # Finding partitions on Raw Data DataFrame
        self.partition_finder()

        # Calling modules/feature_engineering.py for calculating new dataframe
        # The last parameters represent array size of feature for each row in dataframe
        # If you want to change of size, you can change the value
        with open("math_constant/size.json") as f:
            size_values = json.load(f)
        feature_dict_array = label_extractor(self.df, self.contraction_list, size_values["0"], size_values["1"])
        
        for index, row in enumerate(feature_dict_array):
            row["match_day"] = self.match_day
            row["match_frequency"] = self.match_frequency
            row["subject"] = self.subject_name
            row["subject_id"] = self.player_id
            row["timestamp"] = self.training_time
            row["training_name"] = self.training_folder_name

        self.created_df = pd.DataFrame(feature_dict_array)
        if self.test_mode:
            self.created_df.to_pickle("test/featured.pkl")
            print("Saved successfully to test/featured.pkl")
        else:
            print(self.target_training_file_path)
            self.created_df.to_pickle(self.target_training_file_path)
            print("Saved successfully to " + self.target_training_file_path)