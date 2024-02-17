import pandas as pd
import pickle

with open("D:/Dönem Bitirme Projesi/raw_DATA\PKL\Adam_Forshaw/training3__2022-03-14/labeled.pkl", 'rb') as f:
    df = pickle.load(f)

for count,row in df.iterrows():
    if not row["label"] == 1:
        print(row)
"""
for index in range(0,len(df.index)):
    if len(df["R_BL_MNF"][index]) != 150:
        print("ERROR R_BL_MNF " , len(df["R_BL_MNF"][index]))
    elif len(df["L_BL_MNF"][index]) != 150:
        print("ERROR L_BL_MNF")
"""