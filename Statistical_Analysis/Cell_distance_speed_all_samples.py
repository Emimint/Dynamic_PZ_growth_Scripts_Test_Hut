#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python version: Python 2.7.15rc1

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

dest_path = "C:/Users/bell1/Desktop/test"
sample_type = "flower"; #flower or leaf
day_or_night = "all"; # day_formed_primordia, night_formed_primordia or all (samples)
option = "Speed" # choose file and set the y scale according to Speed or Cell_distance
plot = "combined_relative_deformation" # ##1. PLOT OPTION ## : choose what to plot :Speed,Relative_deformation, Cell_distance, combined_speed, combined_relative_deformation or combined_cell_distance /!\ LEAVE BLANK for correlation /!\
correlation = "" # ##2. CORRELATION OPTION ## : _all_data_, BF_0, BF_minus_1 or BF_1./!\ LEAVE BLANK = no correlation /!\ 
if(correlation):
    option = "Speed"
if(sample_type == "flower"):
    if(option =="Speed"):
        data_path = "C:/Users/bell1/Desktop/flower_distance/All_FLOWER_samples_boundary_to_center_distance_info_speed_Relative_deformation.csv"
    if(option =="Cell_distance"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_samples_boundary_to_center_distance_w_BF_info.csv"

if(sample_type == "leaf"):
    if(option =="Speed"):
        data_path = "C:/Users/bell1/Desktop/leaf_distance/All_LEAF_samples_boundary_to_center_distance_info_speed_Relative_deformation.csv"
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
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_samples_boundary_distance_VS_BF_value.png")
    ax.figure.savefig(out_file_name,transparent=True)

if(plot == "Relative_deformation"):
    # # # Relative_deformation plot:
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig = plt.gcf()
    fig.set_size_inches(12, 9)
    ax = sns.lineplot(data=In_use_df, x="BF_value", y="Relative_deformation", hue="Sample_Primordium",legend= None)
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_samples_Relative_deformation_VS_BF_value.png")
    ax.figure.savefig(out_file_name,transparent=True)

if(plot == "Speed"):
    # # # Speed plot:
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig1 = plt.gcf()
    fig1.set_size_inches(12, 9)
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

if(plot == "combined_relative_deformation"):
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig1 = plt.gcf()
    fig1.set_size_inches(12, 9)
    ax1 = sns.lineplot(data=In_use_df, x="BF_value", y="Relative_deformation",color = colour, ci="sd")
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_combined_samples_relative_deformation_VS_BF_value.png")
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

    