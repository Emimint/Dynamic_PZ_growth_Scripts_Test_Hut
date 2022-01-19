#!/usr/bin/env python
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
import selectFiles # on choisit, en fonction des timepoints et des parametres choisis, les fichiers necessaires.
import LineageCombine

"""

	20/08/18: 
	Script done under Python 2.7.12.

	Backzoning is a method to assign zones at a past timepoint using a future timepoint zone information and the cell lineage history between both timepoints.
	
	How-to use in command line: "python BackZoning.py"
    
    The script will create two folders with:
        - the complete lineage information between the current and past timepoint (See LineageCombine for details)
        - the .csv file to use in MGX
	
	In this script, we are using dataframe from pandas library(https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html).

	This script creates a .csv file showing the parents cells part of specific sample (zones) at a given timepoint in the past.
	
	/!\/!\/!\ Example of expecting "zones", parents and lineage file format for this script /!\/!\/!\: 
        - 03_PARENTS_T0T1.csv
		- WT_09_T3_ZONES.csv
		- WT06_LineageCombine_T0T4.csv
	
    21/01/11:
    BackZoning_2_0.py:
    
        - With the option "Zone_Correction", undeterminated cell lineages are automatically labeled.

    21/08/03:

   BackZoning_for_series.py:

       - Serialization of the script (requires a clear path organisation, with separate folders for each sample)
    
"""

path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"
bible_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/210812_all_flower_meristem_boundary_info.csv"
Bible_File_Info = pd.read_csv(bible_path, usecols= [0,1,5]).dropna()
Bible_File_Info.columns = ['Sample','Primordium','Zone_definition_time']
sample_list = list(Bible_File_Info['Sample'].unique())
# current_timepoint_list = list(Bible_File_Info['Time_boundary_formation'].unique())
saving_option = "new_zone_folder" # Choose "in_zone_folder" or "new_zone_folder" : final file will be saved either in a new directory ("in_zone" option) or in the same folder as the zone file ("zone_folder" option).
# ===================================================================

def Zone_Correction(zone_file,lineage_file,BackZoning_info):

    Diff_zones_clones = []
    Diff_zones_clones_new_labels = []
    Underterminated_cell_zone_n_labels = {}

    Zones = pd.read_csv(zone_file).dropna()
    Zones.columns = ['Label' ,'Zone']
    Lineage = pd.read_csv(lineage_file).dropna()
    Lineage.columns = ['Label' ,'Parent_Label']
    Corrected_Zone_File = BackZoning_info
    Corrected_Zone_File.columns = ['Label' ,'Parent_Label']

    df = Lineage.merge(Zones)

    df.drop(['Label'], axis = 1, inplace = True)

    my_unique_labels = list(df['Parent_Label'].unique())

    for val in my_unique_labels:
        clone = df[df['Parent_Label']== val]
        clone_zone_labels = list(clone['Zone'].unique())
        new_zone = sum(clone_zone_labels)

        if len(list(clone['Zone'].unique())) > 1 :
            Diff_zones_clones.append(val)
            Diff_zones_clones_new_labels.append(new_zone)

    Underterminated_cell_zone_n_labels =dict(zip(Diff_zones_clones,Diff_zones_clones_new_labels))
    
    for label in Diff_zones_clones:
        Corrected_Zone_File.loc[(Corrected_Zone_File.Label == label), 'Parent_Label'] = Underterminated_cell_zone_n_labels[label]

    return Corrected_Zone_File

for sample in sample_list:

    sample_number = str(sample).zfill(2)
    path_to_zone = os.path.join(path,sample_number,"OUTPUT","ZONE_PRIMORDIA")
    path_to_parents = os.path.join(path,sample_number,"OUTPUT","PARENTS")
    destination_path = os.path.join(path,sample_number,"OUTPUT")

    list_of_sample_primordia = Bible_File_Info[Bible_File_Info.Sample == sample]['Primordium'].tolist()
    current_timepoint_list = Bible_File_Info[Bible_File_Info.Sample == sample]['Zone_definition_time'].tolist()
    primordium_and_BF_timepoint_list =dict(zip(list_of_sample_primordia,current_timepoint_list))
    
    # for i in primordium_and_BF_timepoint_list:
        # print i, primordium_and_BF_timepoint_list[i]

    for primordium in list_of_sample_primordia:
            
        current_timepoint = primordium_and_BF_timepoint_list[primordium]
        current_timepoint_number = int(current_timepoint[1])
        my_Zone_Parameters = [sample_number+"_"+current_timepoint+"_"+primordium+"_ZONES.csv"]
        # print current_timepoint_number
        # print my_Zone_Parameters[0]
        # continue
        #First, we are looking for the zone file with at the requested timepoint:
        my_zone_file = selectFiles.locate_A_File(my_Zone_Parameters, path_to_zone)
        # print my_zone_file
        # continue

        if not my_zone_file:
            print "\nNo zone file zone found at",current_timepoint,"in",path_to_zone
            continue

        for i in range(0,6): #timepoint
            my_lineage_file=""
            past_timepoint_number = i
            if(current_timepoint_number <= past_timepoint_number):
                # print current_timepoint_number," =< ",past_timepoint_number
                continue
            past_timepoint = "T"+ str(past_timepoint_number)

            # liste of parametres for future file search:
            my_Parent_File_Parameters = [sample_number,current_timepoint,past_timepoint,"PARENTS",".csv"]
            my_Lineage_File_Parameters = [sample_number,current_timepoint,past_timepoint,"_LineageCombine_",".csv"]

            ########################################

            #Then, if the timepoints are consecutive, look for original parenting file:
            if current_timepoint_number == past_timepoint_number+1 :
                my_lineage_file = selectFiles.locate_A_File(my_Parent_File_Parameters, path_to_parents)
                
            else:

                #else, we search for all the parenting information between both timepoints(locateParents returns a list of files), then create the combined lineage files:
                New_Path = LineageCombine.CombineLineage(sample_number,selectFiles.locateParents(sample_number,past_timepoint,current_timepoint,path_to_parents),destination_path)
                my_lineage_file = selectFiles.locate_A_File(my_Lineage_File_Parameters,New_Path)

            if not my_lineage_file:
                print "\nno lineage file found between",past_timepoint,"and",current_timepoint,"in",path_to_parents
                continue                
            # print "\nLineage file found in ", path_to_parents,":\n"
            # print "my_zone_file is ", my_zone_file
            # print "my_lineage_file is ", my_lineage_file
            # print "current_timepoint_number is ", current_timepoint_number
            # print "past_timepoint_number is ", past_timepoint_number 
            # print "+++++++++++++++"
            # continue

            #once both files are found, we can merge them:
            Cell_Lineage = pd.read_csv(my_lineage_file).dropna()
            Cell_Lineage= Cell_Lineage.astype(int)
            Cell_Lineage.columns = ['Label_at_'+ current_timepoint ,'Label_at_'+ past_timepoint]
            # print Cell_Lineage.head(10)

            Zone_Position = pd.read_csv(my_zone_file).dropna()
            Zone_Position= Zone_Position.astype(int)
            Zone_Position.columns = ['Label_at_'+ current_timepoint ,'Zone']
            # print Zone_Position.head(10)

            Cell_Lineage = Cell_Lineage.merge(Zone_Position, on=Cell_Lineage.columns[0])
            # print "\nMerged table:"
            # print Cell_Lineage.head(10)

            #we remove unwanted column here:
            Cell_Lineage = Cell_Lineage.drop(columns='Label_at_'+ current_timepoint)
            Cell_Lineage.columns = ['Label' ,' Parent Label']

            # removal of duplicate rows in final table:
            Cell_Lineage.drop_duplicates(inplace = True)

            # print "\nFinal table:"
            # print Cell_Lineage.head(10)

            Cell_Lineage = Zone_Correction(my_zone_file,my_lineage_file,Cell_Lineage)

            print Cell_Lineage.head(5)

            if (saving_option == "new_zone_folder"):
                #creation of BackZoning output directory:
                timestamp = str(datetime.now().date()).replace("-","")[2:]
                New_Directory = timestamp+"_"+"BACKZONING_RESULTS"
                path_to_New_Directory = os.path.join(destination_path,New_Directory)

                if os.path.exists(path_to_New_Directory):
                    print ("\nThe directory %s already exits in %s" % (New_Directory,destination_path))
                else:
                    try:
                        os.mkdir(path_to_New_Directory)
                    except OSError:  
                        print ("\nCreation of the directory %s failed" % New_Directory)
                        exit()
                    else:  
                        print ("\nSuccessfully created the directory %s in %s " % (New_Directory,destination_path))
                #the resulting backzoning information is then converted in .csv for use in MGX:
                Cell_Lineage.to_csv(os.path.join(path_to_New_Directory,sample_number + "_BackZoning_" + past_timepoint +  current_timepoint + ".csv"), index = False)

            if(saving_option == "in_zone_folder"):
                Cell_Lineage.to_csv(my_zone_file.replace("T"+str(current_timepoint_number),"T"+str(past_timepoint_number)), index=False)
