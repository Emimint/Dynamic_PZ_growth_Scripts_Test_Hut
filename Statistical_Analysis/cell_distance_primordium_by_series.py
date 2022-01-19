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
"xx_xx_sample__Cell_distance_VS_BF_value_by_Primordium.png":

sample_type =#flower of leaf
zone_selection = ""
x_value = "BF_value"
y_value = "Cell_distance"
hue_value = "Primordium"
option = "cell_distance"


****
"xx_xxx_sample_xxx_Growth_VS_BF_value_by_Primordium.png":

sample_type =#flower of leaf
zone_selection = # APZ, boundary or primordium
x_value = "BF_value"
y_value = "Growth"
hue_value = "Primordium"
option = "zone_growth"


****
"xx_xxx_sample__Relative_deformation_VS_BF_value_by_Primordium.png":

sample_type =#flower of leaf
zone_selection = ""
x_value = "BF_value"
y_value = "Relative_deformation"
hue_value = "Primordium"
option = "Relative_deformation"
"""
sample_type = "flower" #flower of leaf
dest_path = "/home/user/Desktop/Project_2/210915_DYN_PZ_PROJECT_STATs"
zone_selection = "" # APZ, boundary, primordium or blank.
x_value = "BF_value" # Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, BF_value
y_value = "Relative_deformation" # Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, BF_value
hue_value = "Primordium" # Primordium, Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, BF_value
option = "Relative_deformation" # cell_distance, zone_cell_dist_growth, Relative_deformation or zone_growth.

if(sample_type == "leaf"):
    if(option =="zone_cell_dist_growth"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_distance_and_growth_information.csv"
    if(option =="zone_growth"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_growth_information_w_BF_values.csv"
    if(option =="cell_distance"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_samples_boundary_to_center_distance_w_BF_info.csv"
    if(option =="Relative_deformation"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_samples_boundary_to_center_distance_info_speed_Relative_deformation.csv"

if(sample_type == "flower"):
    if(option =="zone_cell_dist_growth"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_distance_and_growth_information.csv"
    if(option =="zone_growth"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_growth_information_w_BF_values.csv"
    if(option =="cell_distance"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_samples_boundary_to_center_distance_w_BF_info.csv"
    if(option =="Relative_deformation"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_samples_boundary_to_center_distance_info_speed_Relative_deformation.csv"
# ========================================

if (sample_type == "flower"):
    sample_list = [1,2,19,22] # flower samples
else:
    sample_list = [1,3,6,8] # leaf samples

for sample_number in sample_list:

    Data_File = pd.read_csv(data_path).dropna()
    #remove unwanted values:
    if(option == "cell_distance"):
        Data_File = Data_File[Data_File.Cell_distance != 0]

    if(option == "zone_cell_dist_growth" or option == "zone_growth"):
        Data_File = Data_File[Data_File.Zone != "1000"]
        Data_File["Growth"] = (Data_File["Growth"]-1)*100

    if(option == "zone_cell_dist_growth" or option == "Relative_deformation"):
        Data_File = Data_File[Data_File.Cell_distance != 0]
        Data_File = Data_File[Data_File.Cell_distance_Tn_1 != 0]
        Data_File = Data_File[Data_File.Speed != 0]
        Data_File["Speed"] = Data_File["Speed"]*100
        Data_File = Data_File[Data_File.Relative_deformation != 0]

    # # Data selection:
    Data_File = Data_File[Data_File.Sample_number == sample_number]
    # # Zone selection:
    if(zone_selection):
        Data_File = Data_File[Data_File.Zone == zone_selection]

    primordia_list = list(Data_File['Primordium'].unique())
    primordia_list.sort()

    palette=['lime','blue','gold','fuchsia','cyan']

    if (len(primordia_list) == 4):
        palette=['lime','blue','gold','fuchsia']

    if (len(primordia_list) == 3 and sample_type == "leaf"):
        palette=['blue','gold','fuchsia']

    if (len(primordia_list) == 3 and sample_type == "flower"):
        palette=['lime','blue','gold']

    Data_File = Data_File.sort_values('Primordium')

    print (Data_File.head(60))
    # exit()

    plt.figure()
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig = plt.gcf()
    fig.set_size_inches(12, 9)
    if(y_value == "Growth" and (zone_selection == "APZ") and sample_type == "leaf"):
        plt.ylim(0, 80)
    if(y_value == "Growth" and (zone_selection == "APZ") and sample_type == "flower"):
        plt.ylim(0, 50)
    if(y_value == "Growth" and (zone_selection == "boundary") and sample_type == "leaf"):
        plt.ylim(-100, 100)
    if(y_value == "Growth" and (zone_selection == "boundary") and sample_type == "flower"):
        plt.ylim(-50, 50)
    if(y_value == "Growth" and (zone_selection == "primordium") and sample_type == "leaf"):
        plt.ylim(20, 200)
    if(y_value == "Growth" and (zone_selection == "primordium") and sample_type == "flower"):
        plt.ylim(10, 130)
    ax = sns.lineplot(data=Data_File, x=x_value, y=y_value, hue=hue_value,palette=palette, markers=True, legend="full",ci=None)
    out_file_name = os.path.join(dest_path,str(sample_number) +"_"+sample_type+"_sample_"+zone_selection+"_"+y_value+"_VS_"+x_value+"_by_"+hue_value+".png")
    ax.figure.savefig(out_file_name,transparent=True)


