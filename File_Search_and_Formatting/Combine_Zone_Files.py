#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import pandas as pd


"""
20/02/18:

Script to combine zone files information. A column with the name of the primordium is added.

The files are organised as described here: {new link HERE}

INPUT:
======

Zone files: zone information for each primordium (boundary, APZ - Adjacent Peripheral Zone -, primordia). Zone files are named, for example, as "01_T0_P1_ZONES.csv": zone information for primordium P1 are T0 for sample 01.

OUTPUT:
=======
Combined zones information files (.csv) at one timepoint.

"""
sample_type = "leaf" # "leaf" or "flower"
if(sample_type == "leaf"):
    sample_list = ["01","03","06","08"] #leaf samples
    path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"
else:
    sample_list = ["01","02","19","22"] #flower samples
    path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"
# ========================================
P_values = ["P1","P2","P3","P4","P5"] # maximum number of primordia by series
boundary_values = [[12,11,32,33],[14,12,34,36],[16,13,36,39],[18,14,38,42],[20,15,40,45]]
boundary_dict = dict(zip(P_values,boundary_values))
primordia_dict = dict(zip(P_values,[1,2,3,4,5]))
APZ_dict = dict(zip(P_values,[21,22,23,24,25]))

for sample_number in sample_list:

    zone_path=os.path.join(path, sample_number,"OUTPUT","ZONE_PRIMORDIA")
    dest_path=os.path.join(path, sample_number,"OUTPUT","ZONE_PRIMORDIA","COMBINED_ZONES")

    for i in range(0,6):# we have a maximum of 7 timepoints for each series of this project.

        timepoint = "T"+str(i)

        combined_file_name = sample_number +"_" + timepoint + "_combined_ZONES.csv"

        combined_file_path = os.path.join(dest_path, combined_file_name)

        Combined_File = pd.DataFrame(columns=['Label','Zone','Primordium'])

         
        for file in os.listdir(zone_path):
            if(file.endswith("_ZONES.csv")):
                if (timepoint in file):
                    File = pd.read_csv(os.path.join(zone_path,file)).dropna()
                    File.columns = ['Label' ,'Zone']
                    primordium = file[6:8]
                    File['Primordium'] = primordium
                    Combined_File = pd.concat([Combined_File, File], sort=False)

        print ("The final combined_df for ", sample_number," is:\n")
        print (Combined_File.head())
        print (Combined_File.describe())
        Combined_File = Combined_File.drop_duplicates()

        if(not Combined_File.empty):
            Combined_File = Combined_File[Combined_File.Zone != 0]
            
            for PI in P_values:
                Combined_File.loc[( (Combined_File['Primordium'] == PI) & (Combined_File['Zone'] == primordia_dict[PI] )),'Zone'] = "primordium"
                Combined_File.loc[( (Combined_File['Primordium'] == PI) & (Combined_File['Zone'] == APZ_dict[PI] )),'Zone'] = "APZ"
                for bdy in boundary_dict[PI]:
                    Combined_File.loc[( (Combined_File['Primordium'] == PI) & (Combined_File['Zone'] == bdy)),'Zone'] = "boundary"
            Combined_File.to_csv(combined_file_path, index=False)
