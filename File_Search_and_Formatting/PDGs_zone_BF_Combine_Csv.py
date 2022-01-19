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
import selectFiles

"""
Script to create a single .csv file with PDGs, anisotropy and corresponing BF values.


"""
sample_type = "LEAF"# LEAF or FLOWER 
if(sample_type == "LEAF"):
    sample_list = ["01","03","06","08"] #leaf samples
    path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"
else:
    sample_list = ["01","02","19","22"] #flower samples
    path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"
outfilename = "ALL_"+sample_type+"_cell_PDGs_zone_BF_values.csv"
# ============================================
Combined_DF = pd.DataFrame()
timepoint_list = range (0,6)
bf_Dict_file = selectFiles.locate_A_File(["_BF_dictionaries.csv"],path)
Bf_Dict_File = pd.read_csv(bf_Dict_file).dropna()

for sample_number in sample_list:

    combined_file_path = os.path.join(path, sample_number, "OUTPUT","ZONE_PRIMORDIA","COMBINED_ZONES")
    pdg_path = os.path.join(path, sample_number, "OUTPUT","PDGs_ANISOTROPY")
    
    for i in timepoint_list:
        combined_file = selectFiles.locate_A_File(["T"+str(i)+"_combined_ZONES.csv"],combined_file_path)
        pdg_file = selectFiles.locate_A_File([sample_number+"_T"+str(i)+"_T","_PDGs.csv"],pdg_path)
        
        if(combined_file and pdg_file):
            Combined_File = pd.read_csv(combined_file).dropna()
            Combined_File['Sample_number']= int(sample_number)
            Combined_File['Timepoint']= "T"+str(i)

            Pdg_File = pd.read_csv(pdg_file).dropna()
            print (Combined_File.head(60))
            print (Pdg_File.head(60))
            DF = pd.merge(Combined_File,Pdg_File, on=['Label'])
            Final_DF = pd.merge(DF,Bf_Dict_File, on=['Sample_number','Timepoint','Primordium'])
            Combined_DF = pd.concat([Combined_DF, Final_DF], sort=False)
print ("The final combined_df is:\n")
print (Combined_DF.head(60))
print (Combined_DF.tail(60))
# exit()
Combined_DF.to_csv(os.path.join(path,outfilename), index=False)
