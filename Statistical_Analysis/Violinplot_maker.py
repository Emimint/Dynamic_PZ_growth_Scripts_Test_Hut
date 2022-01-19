#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python version: Python 2.7.15rc1

import csv
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import subprocess
import shutil

"""
To change plot element colors: https://matplotlib.org/3.1.1/gallery/color/named_colors.html

Change palette: https://python-graph-gallery.com/197-available-color-palettes-with-matplotlib/
    
"""

filename = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/ALL_LEAF_growth_night_samples_all_zones_BF_values.csv"
dest_path = '/home/user/Desktop'

File_Info = pd.read_csv(filename).dropna()
# File_Info = File_Info[File_Info.Zone.isin(["boundary","APZ","primordium"])]
# File_Info = File_Info[File_Info.BF_value.isin([-4,-3,-2])]
# File_Info.loc[(File_Info['Zone'] == "boundary"),'Zone'] = "primordium+boundary"
# File_Info.loc[(File_Info['Zone'] == "primordium"),'Zone'] = "primordium+boundary"

File_Info = File_Info[File_Info.Zone.isin(["CZ", "APZ"])]

File_Info = File_Info.sort_values('Zone')

print(File_Info)
# # print File_Info1
# # print Final_DF
# print (File_Info['Label'].duplicated())
# print (File_Info['Label'].unique())
# print (len(File_Info['Label'].unique()))
# print (len(File_Info['Label'].duplicated()))
# exit()
kwargs = {'edgecolor': "black",  # for edge color
          'linewidth': 0.3,
          'size': 1.5  # line width of spot
          }
ax = sns.violinplot(x='BF_value', y='Growth', data=File_Info, hue="Zone", inner=None,
                    palette=['royalblue', 'darkorange'], scale="count", linewidth=0.5)
ax = sns.swarmplot(x="BF_value", y="Growth", data=File_Info, hue="Zone", dodge=True, **kwargs, palette=['grey', 'grey'],
                   alpha=0.8)  # violinplot or boxplot

fig = plt.gcf()
ax.get_legend().remove()

# fig.subplots_adjust(bottom=1)

# plt.show()
# exit()
# out_file_name = os.path.join(dest_path,"all_samples_meristem_zones_overall_growth_violinplot_CZ_PZ.png")
out_file_name = os.path.join(dest_path, "Growth_CV_vs_APZ_by_BF_catplot_violinplot_colored_violins.png")
# plt.show()
ax.figure.savefig(out_file_name, transparent=True, dpi=300)