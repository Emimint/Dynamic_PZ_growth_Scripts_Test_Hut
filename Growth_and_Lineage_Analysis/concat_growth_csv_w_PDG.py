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
An alternative version of the "2__Combine_Zone_Growth_Distance_Csv.py" script to combine zone files (with primordia info) with growth files for each primordia. Here, for night formed samples only.

"""
sample_type = "LEAF"# LEAF or FLOWER 
if(sample_type == "LEAF"):
    path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"
    sample_list = ["01","03","06","08"]
    # sample_list = ["03"]
if(sample_type == "FLOWER"):
    path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"
    sample_list = ["01","02","19","22"]
day_or_night = "night_formed_primordia"; # day_formed_primordia, night_formed_primordia or all (samples)
outfilename = sample_type+"_growth_PDG_"+day_or_night+"_samples_and_zones_w_BF_values.csv"

# ========================================
filter_dict = dict(zip(["day_formed_primordia","night_formed_primordia"],[1,0]))

def locate_A_File(File_Parameters,path):

	my_file=""
	# print "\nExecuting locateFile\n"
	# print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
			# print "Found:",my_file
	# print "\nEnd locateFile\n"
	return my_file

Combined_DF = pd.DataFrame()
bf_Dict_file = locate_A_File(["_BF_dictionaries.csv"],path)
Bf_Dict_File = pd.read_csv(bf_Dict_file).dropna()
PDG_file = locate_A_File(["cell_PDGs_zone_BF_values.csv"],path)
PDG_File = pd.read_csv(PDG_file).dropna()

for sample_number in sample_list:

    growth_path = os.path.join(path, sample_number, "OUTPUT","GROWTH")
    combined_file_path = os.path.join(path, sample_number, "OUTPUT","ZONE_PRIMORDIA","COMBINED_ZONES")

    for i in range(0,6):

        timepoint = "T"+str(i)

        first_file= locate_A_File([timepoint+"_combined_ZONES.csv"],combined_file_path)
        second_file= locate_A_File ([sample_number +"_"+ timepoint,"_GROWTH.csv"],growth_path)#my data
        print (first_file)
        print (second_file)
        # second_file= locate_A_File ([sample_number +"_"+ timepoint,"_GROWTH.csv"],os.path.join(file_path,"GROWTH"))#AG data

        #####################

        if(first_file and second_file):
            First_File = pd.read_csv(first_file).dropna()
            First_File['Sample_number']= int(sample_number)
            First_File['Timepoint']= "T"+str(i)

            Second_File = pd.read_csv(second_file, usecols = ['Label','Value']).dropna()
            Second_File.columns = ['Label' ,'Growth']
            Second_File['Label'] = pd.to_numeric(Second_File['Label'])
            # Conversion of growth in percentage:
            Second_File['Growth'] = Second_File['Growth'].apply(lambda x: (x - 1)*100)
            # Second_File=Second_File.sort_values(by='Growth')

            Combined_File = pd.merge(First_File,Second_File, on=['Label'])
            Combined_DF = pd.concat([Combined_DF, Combined_File], sort=False)

Final_DF = pd.merge(Combined_DF,PDG_File, on=['Label','Zone','Primordium','Sample_number','Timepoint'])
if(day_or_night in ["day_formed_primordia", "night_formed_primordia"]):
    Final_DF = Final_DF[Final_DF.Day_or_night == filter_dict[day_or_night]]
# print ("outfilename is ",outfilename)
# print (Combined_DF.head(20))
# print (Final_DF.head(20))
# exit()
Final_DF.to_csv(os.path.join(path,outfilename), index=False)