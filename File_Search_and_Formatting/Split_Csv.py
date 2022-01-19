#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import pandas as pd


## Used to slip the Combined_DF .csv file made with the Growth_grouped_primordium.py script.

first_file="/home/user/Desktop/Combined_DF.csv"

out_file = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/result.csv"

First_File = pd.read_csv(first_file).dropna()
First_File["Label"] = First_File["Label"].astype(str)
First_File['Min_x'] = First_File['Min_x']*100
First_File['Max_x'] = First_File['Max_x']*100
First_File['Aniso'] = First_File['Aniso']*100

print (First_File)

sample_list = list(First_File['Sample_number'].unique())
sample_list.sort()

for i in sample_list:
    Data = First_File[First_File.Sample_number == i]
    timepoint_list = list(Data['Timepoint'].unique())
    print (timepoint_list)
    # exit()
    for j in timepoint_list:
        Data_T = Data[Data.Timepoint == j]
        primo_list = list(Data['Primordium'].unique())
        for k in primo_list: 
            Data_P = Data_T[Data_T.Primordium == k]
            
            print (Data_P.dtypes)
            # exit()
            Data_P = Data_P[['Label','Min_x','Max_x','Aniso']]
            Data_P.to_csv(os.path.join(out_file,str(i) +"_"+j+"_"+k+"_mean_pdgs_aniso.csv"), index=False)
