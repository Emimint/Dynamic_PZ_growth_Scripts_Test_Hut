#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python version: Python 2.7.15rc1

import pandas as pd
from scipy.stats import ks_2samp

"""
KS test for growth between APZ and CZ cells.   
"""

filename = "C:/Users/bell1/Desktop/leaf_distance/ALL_LEAF_growth_night_samples_all_zones_BF_values.csv"
dest_path = '/home/user/Desktop'

File_Info = pd.read_csv(filename).dropna()

File_Info = File_Info[File_Info.Zone.isin(["CZ","APZ"])]

File_Info = File_Info.sort_values('Zone')

print (File_Info)


Stats = File_Info.groupby(["Zone", "BF_value"])["Growth"].describe() # return all stats between the groups
Stats_List_of_Lists = File_Info.groupby(["Zone", "BF_value"])["Growth"].apply(list) # convert the groups into a list of lists.
Stats_List_of_Lists_APZ = (File_Info[File_Info.Zone.isin(["APZ"])]).groupby(["Zone", "BF_value"])["Growth"].apply(list) # convert the groups into a list of lists for all APZ growth values only.
Stats_List_of_Lists_CZ = (File_Info[File_Info.Zone.isin(["CZ"])]).groupby(["Zone", "BF_value"])["Growth"].apply(list) # convert the groups into a list of lists for all CZ growth values only.

print (Stats_List_of_Lists)
print (Stats_List_of_Lists_APZ)
print (Stats_List_of_Lists_CZ)

for i, j in zip(Stats_List_of_Lists_APZ, Stats_List_of_Lists_CZ):
    print (len(i), len(j), ks_2samp(i,j))

