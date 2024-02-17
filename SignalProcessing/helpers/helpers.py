import os
import sys
import json
import pandas as pd
import pickle


def player_id_founder(player_name, db_player_list):
    for players in db_player_list:
        if players["name"] == player_name:
            player_id = players["id"]
            return player_id
    print("System didn't find this player ", player_name)
    yes_or_no_input = input("Would you like to continue ? [Y \ N] : ")

    if yes_or_no_input == "Y" or yes_or_no_input == "y":
        return ""
    else:
        sys.exit()


def subject_db_checker(player_id):
    try:
        subject_database = json.load(open("jsonFiles/subject_database.json"))
    except:
        print("jsonFiles/subject_database.json does not exist please create that file")
        sys.exit()

    is_player_found = False
    for players in subject_database:
        if players["id"] == player_id:
            subject_name = players["name"]
            is_player_found = True
            print("Subject is already exists : ", subject_name + " / Starting Calculation")
            return subject_name
    if not is_player_found:
        if len(subject_database) == 0:
            subject_name = "Subject_1"
            created_dict = {"name": subject_name, "id": player_id}
            subject_database.append(created_dict)
            with open("jsonFiles/subject_database.json", "w") as subject_database_file:
                json.dump(subject_database, subject_database_file)
            print("New Subject Added Into Database : ", subject_name, " / Starting Calculation")
            return subject_name
        else:
            latest_subject = subject_database[-1]["name"]
            latest_subject = latest_subject.split("_")

            # latest_subject[0] = subject name (Subject)
            # latest_subject[1] = subject number (1,2,3,4)

            latest_subject_number = int(latest_subject[1])
            new_subject_number = latest_subject_number + 1
            subject_name = latest_subject[0] + "_" + str(new_subject_number)
            created_dict = {"name": subject_name, "id": player_id}
            subject_database.append(created_dict)
            with open("jsonFiles/subject_database.json", "w") as subject_database_file:
                json.dump(subject_database, subject_database_file)

            print("New Subject is Added Into Database : ", subject_name, " / Starting Calculation")
            return subject_name


def match_day_calculator(training_date):
    with open("jsonFiles/matchdates.json") as json_file:
        match_dates = json.load(json_file)

    final_delta = -200
    tmp_delta = 0
    for idx, i in enumerate(match_dates):
        dt = pd.to_datetime(i, format="%Y/%m/%d")
        dt1 = pd.to_datetime(training_date, format="%Y/%m/%d")

        delta = (dt1 - dt).days
        if -3 <= delta <= 3:
            if abs(delta) < abs(tmp_delta):
                final_delta = delta
        tmp_delta = delta
    return final_delta

def match_frequency_counter(training_date):
    with open("jsonFiles/matchdates.json") as json_file:
        match_dates = json.load(json_file)

    final_delta = -200
    tmp_delta = 0
    match_frequency_count = 0
    for idx, i in enumerate(match_dates):
        dt = pd.to_datetime(i, format="%Y/%m/%d")
        dt1 = pd.to_datetime(training_date, format="%Y/%m/%d")

        delta = (dt1 - dt).days
        if 0 < delta <= 21:
            match_frequency_count = match_frequency_count + 1
        tmp_delta = delta
    return match_frequency_count

def merge_training_subject_system(save_address):
    print("Merging operation is starting for all subject")
    data_files = os.listdir(save_address)
    for subject_file in data_files:
        if subject_file == "merged":
            continue
        merged_dataFrame = pd.DataFrame()
        training_date_dict = []
        output_training_date_json = {}
        current_subject_address = save_address + "/" + subject_file
        training_files = os.listdir(current_subject_address)
        for training_file in training_files:
            if training_file == "merged":
                continue
            pkl_data_file = current_subject_address + "/" + training_file + "/featured.pkl"
            print(pkl_data_file)
            splitted_training_name = training_file.split("__")
            training_folder_name = splitted_training_name[0]
            training_date_name = splitted_training_name[1]
            training_dict = {"Training Name ": training_folder_name, "Training Time ": training_date_name}
            with open(pkl_data_file, 'rb') as f:
                t_data = pickle.load(f)
            merged_dataFrame = pd.concat([merged_dataFrame, t_data], ignore_index = True)
            training_date_dict.append(training_dict)

        merged_training_folder = current_subject_address + "/merged"
        if not os.path.exists(merged_training_folder):
            os.umask(0)
            os.makedirs(merged_training_folder)
        merged_training_pkl_file = merged_training_folder + "/merged_featured.pkl"
        merged_dataFrame.to_pickle(merged_training_pkl_file)
        print("Saved Successfully to ", merged_training_pkl_file)
        merged_training_json_file = merged_training_folder + "/merged_training_info.json"
        output_training_date_json["trainings"] = training_date_dict
        with open(merged_training_json_file, "w") as training_json_file:
            json.dump(training_date_dict, training_json_file)
        print("Saved Successfully to ", merged_training_json_file)
    return

def merge_all_training_system(save_address):
    merged_dataFrame = pd.DataFrame()
    data_files = os.listdir(save_address)
    for subject_file in data_files:
        if subject_file == "merged":
            continue
        subject_destination = save_address + "/" + subject_file
        merged_destinaton = subject_destination + "/merged"
        if not os.path.exists(merged_destinaton):
            print("This subject doesn't have merged folder please check that")
            sys.exit()
        merged_file_destination = merged_destinaton + "/merged_featured.pkl"
        with open(merged_file_destination, 'rb') as f:
            t_data = pickle.load(f)
        merged_dataFrame = pd.concat([merged_dataFrame, t_data], ignore_index = True)
    all_merged_folder_destination = save_address + "/merged"
    if not os.path.exists(all_merged_folder_destination):
        os.umask(0)
        os.makedirs(all_merged_folder_destination)
    all_merged_file_destination = all_merged_folder_destination + "/all_merged_featured.pkl"
    merged_dataFrame.to_pickle(all_merged_file_destination)
    print("Merging operation was successfull")
    return