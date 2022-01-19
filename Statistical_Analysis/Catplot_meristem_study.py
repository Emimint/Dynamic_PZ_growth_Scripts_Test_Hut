#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python version: Python 2.7.15rc1

import csv
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
from io import StringIO
import subprocess
import shutil

"""
To change plot element colors: https://matplotlib.org/3.1.1/gallery/color/named_colors.html

Change palette: https://python-graph-gallery.com/197-available-color-palettes-with-matplotlib/
    
"""
sample_number = 1
dest_path = '/home/user/Desktop/210605_FIXED_GRAPHs/210605_CZ_PZ_LEAF'
# filename = os.path.join(dest_path,sample_number +"__zone_and_growth_meristem_all_timepoints.csv")
filename = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/ALL_FLOWER_CZ_PZ_growth_meristem_zone_BF_values.csv"
# ========================================================================

File_Info = pd.read_csv(filename).dropna()

File_Info = File_Info.drop('BF_value',axis=1).drop_duplicates()


if(sample_number):
    File_Info = File_Info[File_Info.Sample_number == sample_number]
# print (File_Info)
# exit()
# ax = sns.lineplot(data=File_Info, x="BF_value", y="Cell_distance", hue="Primordia", legend=False,ci=None)
ax = sns.catplot(data=File_Info, x="Timepoint", y="Growth", hue="Zone", kind="swarm",palette=['r','g'], s= 2.5, legend=None)	
# plt.ylim(0.5, 3)
# plt.ylim(-50, 175)
fig = plt.gcf()
fig.set_size_inches(7, 5)
# ax.figure.savefig(out_file_name+"_lineplot.png",transparent=True,dpi=300)

## CATPLOT INSTRUCTIONS:
# ax = sns.catplot(data=File_Info_copy_2, x="Timepoint", y="Growth", hue="Zone", kind="swarm",palette=['r','g'], s= 2.5, legend=None)	
# plt.ylim(0.5, 4)
# # plt.ylim(-50, 150)
# fig = plt.gcf()
# fig.set_size_inches(7, 5)
# ax.savefig(out_file_name+"_catplot.png",transparent=True,dpi=300)

plt.show()



