#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from sys import argv
import subprocess
import time
from datetime import datetime
import os
import os.path
import csv
import pandas as pd
import numpy as np
import math

"""
20/02/18:

Script to concat or merge 2 .csv files with 2 columns each.

"""

# /!\/!\/!\ Complete these informations and save /!\/!\/!\:
first_file ="/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/FLOWER_all_cell_info_all_samples_all_zones_masterfile.csv"
# second_file="/home/user/Desktop/ROSETTE_LEAF_DATA/20200724_102_PM_YFP_veg_SAM_03/3D/OUTPUT/GROWTH/03_GROWTH_T1T2.csv"
second_file="/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/LEAF_all_cell_info_all_samples_all_zones_masterfile.csv"
combined_file = "211213_all_data_cell_info_all_samples_all_zones_masterfile.csv"
combined_stats_file = "stats.csv"
file_path="/home/user/Desktop/Project_2" # your resulting final destination folder.
col_name1 = 'Label'
col_name2 = ' Parent Label'
col_name3 = 'Value'
##################################

First_File = pd.read_csv(first_file)
First_File["Sample_type"] = "flower"

Second_File = pd.read_csv(second_file)
Second_File["Sample_type"] = "leaf"

Combined_File = pd.concat([First_File, Second_File], sort=False)
print (Combined_File)

# # Move the new column to the first position:
df1 = Combined_File.pop('Sample_type')
Combined_File.insert(0, "Sample_type", df1)

# print (Combined_File.head(20))
# print (Combined_File.head(20))
print (Combined_File)
# exit()
# Combined_File.columns = [col_name1,col_name2,col_name3]

# print Combined_File.groupby(col_name2).describe()

Combined_File.to_csv(os.path.join(file_path, combined_file), index=False)
# Combined_File.groupby(col_name2).describe().to_csv(os.path.join(file_path, combined_stats_file), index=False)
