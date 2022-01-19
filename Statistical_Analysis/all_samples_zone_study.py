#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python version: Python 3.8.8

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
To change plot element colors: https://matplotlib.org/3.1.1/gallery/color/named_colors.html

Change palette: https://python-graph-gallery.com/197-available-color-palettes-with-matplotlib/
    
"""
sample_number = 0 # int. 0 for all samples
dest_path = "C:/Users/bell1/Desktop/test"
sample_type = "leaf"; #flower or leaf
day_or_night = "day_formed_primordia"; # day_formed_primordia, night_formed_primordia or all
param = "Min" # Min, Max or Aniso
color = "colored" # gray or colored
if(sample_type == "leaf"):
    data_path = "C:/Users/bell1/Downloads/ALL_LEAF_cell_PDGs_zone_BF_values.csv"
if(sample_type == "flower"):
    data_path = "C:/Users/bell1/Downloads/ALL_FLOWER_cell_PDGs_zone_BF_values.csv"
# ============================================

Data_File = pd.read_csv(data_path).dropna()

#remove unwanted values:
Data_File = Data_File[Data_File.Zone != "1000"]

Data_File["Sample_Primordium"] = Data_File["Sample_number"].astype(str) +"_"+ Data_File["Primordium"]
list_of_sample_primordia = list(Data_File['Sample_Primordium'].unique())
list_of_sample_primordia.sort()

Data_File = Data_File.sort_values('Sample_Primordium')

# # Day or Night formed_primordia selection:
Day_Sample_Info = Data_File[(Data_File.Day_or_night == 1)]
Night_Sample_Info = Data_File[(Data_File.Day_or_night == 0)]
In_use_df = pd.DataFrame()

In_use_df = Data_File

if(day_or_night == "day_formed_primordia"):
	In_use_df = Day_Sample_Info
if(day_or_night == "night_formed_primordia"):
	In_use_df = Night_Sample_Info

In_use_df = In_use_df.sort_values('Zone')

# # # Mean growth by BF value and zone:
Min_mean = In_use_df.groupby(['Zone','BF_value','Sample_number','Primordium'])['Min'].mean().reset_index()
Min_mean['Min'] = Min_mean['Min'] - 1
Max_mean = In_use_df.groupby(['Zone','BF_value','Sample_number','Primordium'])['Max'].mean().reset_index()
Max_mean['Max'] = Max_mean['Max'] - 1
Min_Max_Ani = pd.merge(Min_mean, Max_mean, on = ['Zone','BF_value','Sample_number','Primordium'])
Min_Max_Ani['Aniso'] = (Min_Max_Ani['Max'] - Min_Max_Ani['Min'] ) / Min_Max_Ani['Max']
Min_Max_Ani['Min'] = Min_Max_Ani['Min'] * 100
Min_Max_Ani['Max'] = Min_Max_Ani['Max'] * 100
Min_Max_Ani['Aniso'] = Min_Max_Ani['Aniso'] * 100

print (Min_mean)
print (Max_mean)
print (Min_Max_Ani)
# exit()
if(sample_number != 0):
    Min_Max_Ani = Min_Max_Ani[Min_Max_Ani.Sample_number == sample_number]

plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
fig = plt.gcf()
fig.set_size_inches(12, 9)

if(sample_type == "flower"):
    if(param == "Aniso"):
        plt.ylim(0, 200)
    if(param == "Min" or param == "Max"):
        plt.ylim(-45, 80)
if(sample_type == "leaf"):
    if(param == "Aniso"):
        plt.ylim(30, 300)
    if(param == "Min" or param == "Max"):
        plt.ylim(-50, 110)

if(color == "gray"):
    ax = sns.lineplot(data=Min_Max_Ani, x="BF_value", y=param,hue="Zone",style="Zone",palette=['black','silver','dimgray'], markers=True, dashes=[(2,0),(1,1),(1,2)], legend=None,ci="sd")
if(color == "colored"):
    ax = sns.lineplot(data=Min_Max_Ani, x="BF_value", y=param,hue="Zone",style="Zone",palette=['darkblue','green','coral'], markers=True, dashes=[(2,0),(1,1),(1,2)], legend=None,ci="sd")


if(sample_number == 0):
    sample_number = ""

out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_"+str(sample_number)+"__mean_"+param+"_vs_boundary_formation_time_"+color+".png")
ax.figure.savefig(out_file_name,transparent=True)
