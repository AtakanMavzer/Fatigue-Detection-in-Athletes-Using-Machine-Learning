from signal_processing import *
from helpers.helpers import *
from helpers.helpers import *


raw_data_folder_name = "raw_DATA"
team_name = "Team1"

test_mode = False

raw_data_address = "../DATA/" + raw_data_folder_name
bucket_save_address = "../DATA/PKL/" + team_name


SP_pkl_v2_class = signal_processing_pkl_v2(raw_data_address, bucket_save_address, test_mode)

SP_pkl_v2_class.data_selector()

merge_training_subject_system(bucket_save_address)

merge_all_training_system(bucket_save_address)