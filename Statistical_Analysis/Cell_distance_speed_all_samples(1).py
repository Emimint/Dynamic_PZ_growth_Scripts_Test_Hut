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
"XXX_XX_PX_growth_by_region_vs_boundary_formation.png":




****
"xxx_xxx_correlation__xxx__boundary_distance_VS_Speed_xxx.png":

sample_type =#flower or leaf
day_or_night =# day_formed_primordia, night_formed_primordia or all (samples)
option = "Speed"
plot = ""
correlation =#_all_data_, BF_0, BF_minus_1 or BF_1.

"""

dest_path = "/home/user/Desktop/Project_2/210915_DYN_PZ_PROJECT_STATs"
sample_type = "leaf"; #flower or leaf
day_or_night = "all"; # day_formed_primordia, night_formed_primordia or all (samples)
option = "Cell_distance" # choose file and set the y scale according to Speed or Cell_distance
plot = "combined_cell_distance" # ##1. PLOT OPTION ## : choose what to plot :Speed, Cell_distance, combined_speed or combined_cell_distance /!\ LEAVE BLANK for correlation /!\
correlation = "" # ##2. CORRELATION OPTION ## : _all_data_, BF_0, BF_minus_1 or BF_1./!\ LEAVE BLANK = no correlation /!\ 
if(correlation):
    option = "Speed"
if(sample_type == "flower"):
    if(option =="Speed"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_samples_boundary_to_center_distance_info_speed_Relative_deformation.csv"
    if(option =="Cell_distance"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_samples_boundary_to_center_distance_w_BF_info.csv"

if(sample_type == "leaf"):
    if(option =="Speed"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_samples_boundary_to_center_distance_info_speed_Relative_deformation.csv"
    if(option =="Cell_distance"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_samples_boundary_to_center_distance_w_BF_info.csv"

colour = "black" # default combined plot color
# ========================================================================

Data_File = pd.read_csv(data_path).dropna()
Data_File["Sample_Primordium"] = Data_File["Sample_number"].astype(str) +"_"+ Data_File["Primordium"]

if(option =="Speed"):
    Data_File = Data_File[Data_File.Speed != 0]
    Data_File = Data_File[Data_File.Cell_distance != 0]
    Data_File = Data_File[Data_File.Relative_deformation != 0]
    Data_File = Data_File[Data_File.Cell_distance_Tn_1 != 0]
    Data_File["Speed"] = Data_File["Speed"]*100

if(option =="Cell_distance"):
    Data_File = Data_File[Data_File.Cell_distance != 0]

if(correlation == "BF_0"):
    Data_File = Data_File[Data_File.BF_value == 0]

if(correlation == "BF_1"):
    Data_File = Data_File[Data_File.BF_value == 1]

if(correlation == "BF_minus_1"):
    Data_File = Data_File[Data_File.BF_value == -1]

# print (Data_File.head(60))
# exit()
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

# print (In_use_df)
print (In_use_df.head(60))
# exit()
list_of_sample_primordia = list(Data_File['Sample_Primordium'].unique())


# # # Plot selection:
if(plot == "Cell_distance"):
    # # # Cell_distance plot:
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig = plt.gcf()
    fig.set_size_inches(12, 9)
    ax = sns.lineplot(data=In_use_df, x="BF_value", y="Cell_distance", hue="Sample_Primordium",legend= "full")
    # ax.set_ylim((In_use_df[option].min() - 10), (In_use_df[option].max() + 10))
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_samples_boundary_distance_VS_BF_value.png")
    ax.figure.savefig(out_file_name,transparent=True)

if(plot == "Speed"):
    # # # Speed plot:
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig1 = plt.gcf()
    fig1.set_size_inches(12, 9)
    # ax1 = sns.lineplot(data=In_use_df, x="BF_value", y="Speed", hue="Sample_Primordium", legend="full", style ="Sample_Primordium", dashes=(((2,1), )*(len(list_of_sample_primordia))))
    ax1 = sns.lineplot(data=In_use_df, x="BF_value", y="Speed", hue="Sample_Primordium", legend="full", style ="Sample_Primordium", dashes= None)
    ax1.set_ylim((In_use_df[option].min() - 10), (In_use_df[option].max() + 10))
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_samples_boundary_displacement_speed_VS_BF_value.png")
    ax1.figure.savefig(out_file_name,transparent=True)

if(plot == "combined_speed"):
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig1 = plt.gcf()
    fig1.set_size_inches(12, 9)
    ax1 = sns.lineplot(data=In_use_df, x="BF_value", y="Speed",color = colour, ci="sd")
    ax1.set_ylim((In_use_df[option].min() - 10), (In_use_df[option].max() + 10))
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_combined_samples_boundary_displacement_speed_VS_BF_value.png")
    ax1.figure.savefig(out_file_name,transparent=True)

if(plot == "combined_cell_distance"):
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig1 = plt.gcf()
    fig1.set_size_inches(12, 9)
    ax1 = sns.lineplot(data=In_use_df, x="BF_value", y="Cell_distance",color = colour, ci="sd")
    ax1.set_ylim((In_use_df[option].min() - 10), (In_use_df[option].max() + 10))
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_combined_samples_boundary_distance_VS_BF_value.png")
    ax1.figure.savefig(out_file_name,transparent=True)

if(correlation):
    fig = plt.gcf()
    fig.set_size_inches(12, 9)
    ax = sns.scatterplot(data=In_use_df, x="Cell_distance", y="Speed",color = colour, legend=None)
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_correlation_"+correlation+"_boundary_distance_VS_Speed.png")
    ax.figure.savefig(out_file_name,transparent=True)

if(correlation):
    fig = plt.gcf()
    fig.set_size_inches(12, 9)
    ax = sns.scatterplot(data=In_use_df, x="Cell_distance", y="Speed",color = colour, legend=None)
    ax = sns.regplot(x="Cell_distance", y="Speed", data=In_use_df,color = colour,ci=None)
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_correlation_"+correlation+"_boundary_distance_VS_Speed_w_regression.png")
    ax.figure.savefig(out_file_name,transparent=True)

    