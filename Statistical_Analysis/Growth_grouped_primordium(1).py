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
"xx_xx___samples_growth_by_region_vs_boundary_formation_xxx.png"

Full x11 color names here: https://en.wikipedia.org/wiki/X11_color_names

****

  
"""
sample_type = "leaf" #flower of leaf
day_or_night = "night_formed_primordia"; # all, day_formed_primordia or night_formed_primordia
option = "yes" #"yes" for colored graphs. Else, leave blank.
data = "Min" #Growth, or Min, Max (i.e. PDGs) or Aniso (i.e. anisotropy)
if(sample_type == "leaf"):
    if(data == "Growth"):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_growth_information_w_BF_values.csv"
    if(data in ["Min","Max","Aniso"]):
        data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/ALL_LEAF_cell_PDGs_zone_BF_values.csv"        
if(sample_type == "flower"):
    if(data == "Growth"):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/All_FLOWER_growth_information_w_BF_values.csv"
    if(data in ["Min","Max","Aniso"]):
        data_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/ALL_FLOWER_cell_PDGs_zone_BF_values.csv"
dest_path = "/home/user/Desktop/Project_2/210915_DYN_PZ_PROJECT_STATs"
# ========================================================================
list_of_palette = [   ['black',  'black','black'], ['gray',  'gray','gray'], ['silver',  'silver','silver'],['red',  'red','red'],['lime',  'lime','lime'],['blue',  'blue','blue'],['purple',  'purple','purple'],['tomato',  'tomato','tomato'],['rebeccapurple',  'rebeccapurple','rebeccapurple'],['darkgreen',  'darkgreen','darkgreen'],['saddlebrown',  'saddlebrown','saddlebrown'],['navy',  'navy','navy'],['mediumseagreen',  'mediumseagreen','mediumseagreen'],['green',  'green','green'],['gold',  'gold','gold'],['chartreuse',  'chartreuse','chartreuse'],['orchid',  'orchid','orchid'],['m',  'm','m'],['violet',  'violet','violet'],['blueviolet',  'blueviolet','blueviolet'],['lightcoral',  'lightcoral','lightcoral'],['cyan',  'cyan','cyan'],['teal',  'teal','teal'],['slateblue',  'slateblue','slateblue']]
# list_of_palette = [   ['black',  'black','black'], ['gray',  'gray','gray'], ['silver',  'silver','silver'],['red',  'red','red'],['lime',  'lime','lime'],['blue',  'blue','blue'],['purple',  'purple','purple'],['tomato',  'tomato','tomato'],['rebeccapurple',  'rebeccapurple','rebeccapurple'],['darkgreen',  'darkgreen','darkgreen'],['saddlebrown',  'saddlebrown','saddlebrown'],['navy',  'navy','navy'],['mediumseagreen',  'mediumseagreen','mediumseagreen'],['green',  'green','green'],['gold',  'gold','gold'],['chartreuse',  'chartreuse','chartreuse'],['orchid',  'orchid','orchid'],['m',  'm','m'],['violet',  'violet','violet'],['blueviolet',  'blueviolet','blueviolet'],['lightcoral',  'lightcoral','lightcoral'],['cyan',  'cyan','cyan'],['teal',  'teal','teal'],['slateblue',  'slateblue','slateblue'],['black',  'black','black'], ['gray',  'gray','gray'], ['silver',  'silver','silver'],['red',  'red','red'],['lime',  'lime','lime'],['blue',  'blue','blue'],['purple',  'purple','purple'],['tomato',  'tomato','tomato'],['rebeccapurple',  'rebeccapurple','rebeccapurple'],['darkgreen',  'darkgreen','darkgreen'],['saddlebrown',  'saddlebrown','saddlebrown'],['navy',  'navy','navy'],['mediumseagreen',  'mediumseagreen','mediumseagreen'],['green',  'green','green'],['gold',  'gold','gold'],['chartreuse',  'chartreuse','chartreuse'],['orchid',  'orchid','orchid'],['m',  'm','m'],['violet',  'violet','violet'],['blueviolet',  'blueviolet','blueviolet'],['lightcoral',  'lightcoral','lightcoral'],['cyan',  'cyan','cyan'],['teal',  'teal','teal'],['slateblue',  'slateblue','slateblue']]

Data_File = pd.read_csv(data_path).dropna()

#remove unwanted values:
Data_File = Data_File[Data_File.Zone != "1000"]

Data_File["Sample_Primordium"] = Data_File["Sample_number"].astype(str) +"_"+ Data_File["Primordium"]
list_of_sample_primordia = list(Data_File['Sample_Primordium'].unique())
primordia_palette =[]

for i in range(0,len(list_of_sample_primordia)):
    new_color_pallette = list_of_palette[i]
    primordia_palette.append(new_color_pallette)

Color_Code = dict(zip(list_of_sample_primordia, primordia_palette))

Data_File = Data_File.sort_values('Sample_Primordium')

if(data == "Growth"):
    Data_File["Growth"] = (Data_File["Growth"]-1)*100


# print (Data_File.head(10))

if(data in ["Min","Max","Aniso"]):
    # # # Mean growth by BF value and zone:
    Min_mean = Data_File.groupby(['Zone','BF_value','Sample_number','Primordium','Sample_Primordium'])['Min'].mean().reset_index()
    Min_mean['Min'] = Min_mean['Min'] - 1
    Max_mean = Data_File.groupby(['Zone','BF_value','Sample_number','Primordium','Sample_Primordium'])['Max'].mean().reset_index()
    Max_mean['Max'] = Max_mean['Max'] - 1
    Min_Max_Ani = pd.merge(Min_mean, Max_mean, on = ['Zone','BF_value','Sample_number','Primordium','Sample_Primordium'])
    Min_Max_Ani['Aniso'] = (Min_Max_Ani['Max'] - Min_Max_Ani['Min'] ) / Min_Max_Ani['Max']
    Combined_DF = pd.merge(Min_Max_Ani, Data_File, on = ['Zone','BF_value','Sample_number','Primordium','Sample_Primordium'])
    Combined_DF.to_csv('/home/user/Desktop/test.csv', index=False)
    Data_File = Data_File.drop(Data_File.columns[[0,5,6,7]], axis = 1).drop_duplicates()
    Data_File = pd.merge(Min_Max_Ani, Data_File, on = ['Zone','BF_value','Sample_number','Primordium','Sample_Primordium'])
    # Data_File = Min_Max_Ani

    print (Min_Max_Ani)
    print (Combined_DF)
    Combined_DF.to_csv("/home/user/Desktop/test.csv", index=False)
print (Data_File)
# exit()

In_use_df = pd.DataFrame()
used_colors = []
primordium_list = []

# """
for echantillon in list_of_sample_primordia:

    if(day_or_night == "day_formed_primordia"):
        Day_Sample_Info = Data_File[(Data_File.Day_or_night == 1)]
        In_use_df = Day_Sample_Info
    if(day_or_night == "night_formed_primordia"):
        Night_Sample_Info = Data_File[(Data_File.Day_or_night == 0)]
        In_use_df = Night_Sample_Info
    if(day_or_night == "all"):
        In_use_df = Data_File
    small_df = In_use_df[(In_use_df.Sample_Primordium == echantillon)]
    small_df = small_df.sort_values('Zone')

    if(option):
        # # Colored graphs:
        # list_of_palette_colors =random.randint(0,23)
        # colormap = list_of_palette[list_of_palette_colors]
        # del list_of_palette[list_of_palette_colors]
        ax = sns.lineplot(data=small_df, x="BF_value", y=data, hue="Zone", style="Zone",palette=Color_Code[echantillon], markers=True, dashes=[(2,0),(1,1),(1,2)], legend=False)
        if(not small_df.empty):
            primordium_list.append(echantillon)
            # used_colors.append(colormap[0])
            used_colors.append(Color_Code[echantillon][0])
    else:
    # # Gray graphs:
        ax = sns.lineplot(data=small_df, x="BF_value", y=data, hue="Zone", style="Zone",palette=['black','silver','dimgray'], markers=True, dashes=[(2,0),(1,1),(1,2)], legend=None,ci=True)

    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    fig = plt.gcf()
    fig.set_size_inches(12, 9)

if(option):
    Color_Primordium = pd.DataFrame(list(zip(primordium_list, used_colors)),columns =['Primordium', 'color'])
    print (Color_Primordium.head(30))
# plt.show()
# exit()

if(option):
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_samples_"+data+"_by_region_vs_boundary_formation_color.png")
    out_file_legend = out_file_name.replace(".png","_legend.csv")
    Color_Primordium.to_csv(out_file_legend,index=False)
else:
    out_file_name = os.path.join(dest_path,day_or_night +"_"+sample_type+"_samples_"+data+"_by_region_vs_boundary_formation_color_gray.png")
ax.figure.savefig(out_file_name,transparent=True)
