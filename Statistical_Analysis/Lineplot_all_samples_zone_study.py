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
"XXX_XX_PX_growth_by_region_vs_boundary_formation.png":

data_path = ".../PATH/All_XXX__growth_information_w_BF_values.csv""
sample_type = #flower or leaf
day_or_night = "all"
   
"""
data_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/All_LEAF_growth_information_w_BF_values.csv"
dest_path = "/home/user/Desktop/Project_2/210915_DYN_PZ_PROJECT_STATs"
sample_type = "leaf"; #flower or leaf
day_or_night = "all"; # all, day_formed_primordia or night_formed_primordia
# # # ===========================================================

Data_File = pd.read_csv(data_path).dropna()
Data_File["Growth"] = (Data_File["Growth"]-1)*100

# print (Data_File.tail(30))
#remove unwanted values:
Data_File = Data_File[Data_File.Zone != "1000"]

# print (Data_File.tail(30))
# exit()

# # Day or Night formed_primordia selection:
Day_Sample_Info = Data_File[(Data_File.Day_or_night == 1)]
Night_Sample_Info = Data_File[(Data_File.Day_or_night == 0)]

if(day_or_night == "day_formed_primordia"):
	Data_File = Day_Sample_Info
if(day_or_night == "night_formed_primordia"):
	Data_File = Night_Sample_Info

sample_list = Data_File.Sample_number.unique()

for sample_number in sample_list:

    In_use_df = Data_File[Data_File.Sample_number == sample_number]

    primordia_list = In_use_df.Primordium.unique()
    
    for primordium in primordia_list:

        new_df = In_use_df[In_use_df.Primordium == primordium]
        new_df = new_df.sort_values("Zone")

        plt.figure()
        plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
        fig = plt.gcf()
        fig.set_size_inches(12, 9)
        ax = sns.lineplot(data=new_df, x="BF_value", y="Growth",hue="Zone",style="Zone",palette=['darkblue','lightgreen','coral'], markers=True, dashes=[(2,0),(1,1),(1,2)], legend="full")
        out_file_name = os.path.join(dest_path,sample_type+"_"+str(sample_number) +"_"+primordium +"_growth_by_region_vs_boundary_formation.png")
        ax.figure.savefig(out_file_name,transparent=True)
