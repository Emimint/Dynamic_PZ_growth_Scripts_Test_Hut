#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python version: Python 2.7.15rc1

import csv
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.pyplot import figure
import seaborn as sns
from io import StringIO
import subprocess
import shutil

"""
Files generated and options:
============================

****
"CORRELATION_GROWTH_APZ_vs_PRIMORDIA" graphs:

"""
dest_path = "/home/user/Desktop/Project_2/210915_DYN_PZ_PROJECT_STATs"
sample_type = "leaf"; #flower or leaf
day_or_night = "night_formed_primordia"; # day_formed_primordia, night_formed_primordia or all (samples)
BF_value = "" #BF_0,  BF_1 or blank.
BF_value_range = ""
# BF_value_range = range(-4,0) #_BF_value_ranging_from_-4_to_-1_
BF_value_range = range(0,2) #_BF_value_ranging_from_0_to_1_
x_value = "Growth_APZ" # Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, BF_value
y_value = "Growth_primordium" # Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, BF_value
plot_type = "regplot" #scatterplot or regplot
if(sample_type == "leaf"):
    data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_growth_information_w_BF_values.csv"

if(sample_type == "flower"):
    data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_growth_information_w_BF_values.csv"

colour = "black" # default combined plot color
# ========================================================================
color_list = ["brown","red","orange","yellow","lime","green","blue","darkblue","indigo"]
BF_values = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
BF_Dictionnary = dict(zip(BF_values, color_list))

Data_File = pd.read_csv(data_path).dropna()
Data_File = Data_File[Data_File.Zone != "1000"]
Data_File = Data_File[Data_File.Zone != "boundary"]
Data_File["Growth"] = (Data_File["Growth"]-1)*100
Data_File["Sample_Timepoint_Primordium"] = Data_File["Sample_number"].astype(str) +"_"+ Data_File["Timepoint"]+"_"+  Data_File["Primordium"]

# # BF_value_range selection:
if(BF_value_range):
    Data_File = Data_File[Data_File.BF_value.isin(BF_value_range)]
    if(BF_value_range == range(0,2)):
        range_name = "0_to_1_"
    if(BF_value_range == range(-4,0)):
        range_name = "minus_4_to_minus_1_"

if(BF_value == "BF_0"):
    Data_File = Data_File[Data_File.BF_value == 0]

if(BF_value == "BF_1"):
    Data_File = Data_File[Data_File.BF_value == 1]

if(BF_value == "BF_minus_1"):
    Data_File = Data_File[Data_File.BF_value == -1]

# # Day or Night formed_primordia selection:
Day_Sample_Info = Data_File[(Data_File.Day_or_night == 1)]
Night_Sample_Info = Data_File[(Data_File.Day_or_night == 0)]

In_use_df = Data_File # if all samples are selected

if(day_or_night == "day_formed_primordia"):
    In_use_df = Day_Sample_Info
    colour = "orange"

if(day_or_night == "night_formed_primordia"):
    In_use_df = Night_Sample_Info
    colour = "darkblue"

In_use_df = In_use_df[['Sample_Timepoint_Primordium','BF_value','Zone','Growth']]
# list_of_sample_timepoint_primordia = list(In_use_df['Sample_Timepoint_Primordium'].unique())
print (In_use_df)
# exit()
# # Make 2 dataframes:
Data_File_APZ = In_use_df[In_use_df.Zone == "APZ"]
Data_File_APZ.columns = ['Sample_Timepoint_Primordium','BF_value','APZ','Growth_APZ']
Data_File_Primordia = In_use_df[In_use_df.Zone == "primordium"]
Data_File_Primordia.columns = ['Sample_Timepoint_Primordium','BF_value','primordium','Growth_primordium']

Combined_Growth = pd.merge(Data_File_APZ,Data_File_Primordia, on = ['Sample_Timepoint_Primordium','BF_value'])

print (Data_File_APZ)
print (Data_File_Primordia)
print (Combined_Growth)
# print (Combined_Growth.tail(60))
# print (Combined_Growth.tail(60))
# exit()
# Combined_Growth = Combined_Growth[Combined_Growth.BF_value > 0]

BF_list = list(Combined_Growth['BF_value'].unique())
BF_list.sort()
print (BF_list)
# exit()


fig = plt.gcf()
fig.set_size_inches(12, 9)

if(plot_type == "scatterplot"):
    for i in BF_list:
        current = Combined_Growth[Combined_Growth.BF_value == i]
        ax = sns.scatterplot(data=current, x=x_value, y=y_value,color = BF_Dictionnary[i], legend=None)
        # ax = sns.scatterplot(data=current, x=x_value, y=y_value,color = "blue", legend=None)
if(plot_type == "regplot"):
    ax = sns.regplot(x=x_value, y=y_value, data=Combined_Growth, robust = True , color = colour,ci=None)

out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_samples_correlation_"+x_value+"_VS_"+y_value+"_"+BF_value+"_w_regression_"+plot_type+".png")
if(BF_value_range):
    out_file_name = out_file_name.replace(sample_type,"_BF_value_ranging_from_"+range_name+"_"+sample_type)
# print (out_file_name)
# exit()
ax.figure.savefig(out_file_name,transparent=True)
# plt.show()

