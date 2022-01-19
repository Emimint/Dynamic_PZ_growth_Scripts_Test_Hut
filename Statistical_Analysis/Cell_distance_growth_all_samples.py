#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python version: Python 3.8.8

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
Files generated and options:
============================

****
"all_xxx_xxx_samples_correlation_Speed_VS_Growth_w_regression.png":

sample_type = #flower or leaf
sample_number = ""
day_or_night = "all"
plot_type = "regplot"
zone_selection = # APZ, boundary, primordium or blank.
BF_value = ""
BF_value_range = ""
x_value = "Speed"
y_value = "Growth"
hue_value = ""
option = "full"

****
"xxx__samples_BF_value_VS_Growth_by_Zone.png":

sample_type = #flower or leaf
sample_number = "" 
day_or_night = # day_formed_primordia, night_formed_primordia or all (samples)
plot_type = "lineplot" 
zone_selection = ""
BF_value = "" 
BF_value_range = ""
x_value = "BF_value" 
y_value = "Growth" 
hue_value = "Zone"
option = ""    
"""

dest_path = "C:/Users/bell1/Desktop/test"
sample_type = "leaf"; #flower or leaf
sample_number = "" # leave blank for combined info.
day_or_night = "night_formed_primordia"; # day_formed_primordia, night_formed_primordia or all (samples)
plot_type = "lineplot" # lineplot or regplot
zone_selection = "" # APZ, boundary, primordium or blank.
BF_value = "" #BF_0,  BF_1 or blank. Optional.
BF_value_range = ""
# BF_value_range = range(-4,0) #_BF_value_ranging_from_-4_to_-1_ .Optional.
# BF_value_range = range(0,2) #_BF_value_ranging_from_0_to_1_ .Optional.
x_value = "BF_value" # Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, BF_value
y_value = "Growth" # Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, BF_value
hue_value = "Zone" # Primordium, Timepoint,Speed, Relative_deformation, Zone, Growth, Cell_distance, Sample_Primordium, Sample_Primordium_Zone, BF_value
option = "" #for complete, full file (file with both cell distance and growth information - i.e. option = "full") or minimalist file (file with growth information - i.e. option is blank).

if(sample_type == "leaf"):
    if(option =="full"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_distance_and_growth_information.csv"
    else:
        data_path = "C:/Users/bell1/Downloads/All_LEAF_growth_information_w_BF_values.csv"

if(sample_type == "flower"):
    if(option =="full"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_distance_and_growth_information.csv"
    else:
        data_path = "C:/Users/bell1/Downloads/All_FLOWER_growth_information_w_BF_values.csv"

# ========================================================================

colour = "black" # default combined plot color

Data_File = pd.read_csv(data_path).dropna()
Data_File["Growth"] = (Data_File["Growth"]-1)*100
Data_File["Sample_Primordium"] = Data_File["Sample_number"].astype(str) +"_"+ Data_File["Primordium"]
list_of_sample_primordia = list(Data_File['Sample_Primordium'].unique())
list_of_sample_primordia.sort()

# # Remove unwanted values:
if(option == "full"):
    Data_File = Data_File[Data_File.Speed != 0]
    Data_File = Data_File[Data_File.Cell_distance != 0]
    Data_File = Data_File[Data_File.Relative_deformation != 0]
    Data_File = Data_File[Data_File.Cell_distance_Tn_1 != 0]
Data_File = Data_File[Data_File.Zone != "1000"]

# # Zone selection:
if(zone_selection):
    Data_File = Data_File[Data_File.Zone == zone_selection]


if(sample_number):
    Data_File = Data_File[Data_File.Sample_number == int(sample_number)]

# # BF_value_range selection:
if(BF_value_range):
    Data_File = Data_File[Data_File.BF_value.isin(BF_value_range)]
    if(BF_value_range == range(0,2)):
        range_name = "0_to_1_"
    if(BF_value_range == range(-4,0)):
        range_name = "minus_4_to_minus_1_"

if(option =="full"):
    Data_File["Speed"] = Data_File["Speed"]*100

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

if(hue_value):
    In_use_df = In_use_df.sort_values(hue_value)
print (In_use_df.head(60))
print (In_use_df.tail(60))
my_list = In_use_df['Zone'].unique()
print (my_list)
# exit()

# # # Plot selection:
if(plot_type == "lineplot"):
    # # # Cell_distance plot:
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig = plt.gcf()
    fig.set_size_inches(12, 9)
    if(hue_value):
        # # With neutral color palette:
        # ax = sns.lineplot(data=In_use_df, x=x_value, y=y_value, hue=hue_value,style="Zone",palette=['black','dimgray',  'silver'], markers=True, dashes=[(2,0),(1,1),(1,2)],legend= "full", ci = "sd")
        ax = sns.lineplot(data=In_use_df, x=x_value, y=y_value, hue="Zone",style="Zone",palette=['darkblue','green','coral'], markers=True, dashes=[(2,0),(1,1),(1,2)],legend= None, ci = "sd")
        if(sample_type == "flower"):
            ax.set_ylim(-60, 120)
        if(sample_type == "leaf"):
            ax.set_ylim(-60, 210)
    else:
        ax = sns.lineplot(data=In_use_df, x=x_value, y=y_value, legend= "full")
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_"+sample_number+"_samples_"+x_value+"_VS_"+y_value+"_by_"+hue_value+".png")
    ax.figure.savefig(out_file_name,transparent=True)


if(plot_type == "regplot"):
    fig = plt.gcf()
    fig.set_size_inches(12, 9)
    ax = sns.regplot(x=x_value, y=y_value, data=In_use_df, robust = True , color = colour,ci=None)
    out_file_name = os.path.join(dest_path,day_or_night +"_"+zone_selection+"_"+sample_type+"_samples_correlation_"+x_value+"_VS_"+y_value+"_w_regression.png")
    if(BF_value_range):
        out_file_name = os.path.join(dest_path,day_or_night +"_"+zone_selection+"_BF_value_ranging_from_"+range_name+"_"+sample_type+"_samples_correlation_"+x_value+"_VS_"+y_value+"_w_regression.png")
    ax.figure.savefig(out_file_name,transparent=True)

    