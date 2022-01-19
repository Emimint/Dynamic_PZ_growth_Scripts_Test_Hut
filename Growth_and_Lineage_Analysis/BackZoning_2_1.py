#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import os
import os.path
import pandas as pd
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
    BackZoning_2_1.py:
    
        - Undeterminated cells at intersecting zones are given specific labels:
        for example, if mother cell progeny is in zone 22 and zone 4, the mother cell zone label will be 22 + 4 ==> 26.
        - Final file can be saved in a new folder or in same location as zone info file. 
	
    
"""
my_lineage_file=""
sample_number = "22"
current_timepoint_number = 4
past_timepoint_number = 3
path_to_zone = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/22/OUTPUT/ZONE_PRIMORDIA"
path_to_parents = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/22/OUTPUT/PARENTS"
destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/22/OUTPUT"
search_str = "P1_ZONES" # str used for search of the zone file.
option = "zone_specific_label" # "zone_specific_label" or "unspecific_zone_label".
undeterminated_zone_label = "1" # single label for undeterminated zone, i.e. clonal region with fate shared between organ regions. If the option "unspecific_zone_label" is chosen above, assign any desired numerical value, starting 0. Can be left blank (i.e. "") if option "zone_specific_label" is chosen instead.
saving_option = "new_zone_folder" # Choose "in_zone_folder" or "new_zone_folder" : final file will be saved either in a new directory ("in_zone" option) or in the same folder as the zone file ("zone_folder" option).
# # =============================================


# liste of parametres for future file search:
current_timepoint = "T"+ str(current_timepoint_number)
past_timepoint = "T"+ str(past_timepoint_number)
my_Zone_Parameters = [sample_number,current_timepoint,search_str,".csv"]
my_Parent_File_Parameters = [sample_number,current_timepoint,past_timepoint,"PARENTS",".csv"]
my_Lineage_File_Parameters = [sample_number,current_timepoint,past_timepoint,"_LineageCombine_",".csv"]

########################################

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
        if(option == "zone_specific_label"):
            Corrected_Zone_File.loc[(Corrected_Zone_File.Label == label), 'Parent_Label'] = Underterminated_cell_zone_n_labels[label]
        if(option == "unspecific_zone_label"):
            Corrected_Zone_File.loc[(Corrected_Zone_File.Label == label), 'Parent_Label'] = int(undeterminated_zone_label)

    return Corrected_Zone_File

#First, we are looking for the zone file at the requested timepoint:
my_zone_file = selectFiles.locate_A_File(my_Zone_Parameters, path_to_zone)

if not my_zone_file:
	print ("\nNo zone file zone found at",current_timepoint,"in",path_to_zone)
	sys.exit("\nEND of BackZoning")

#Then, if the timepoints are consecutive, look for original parenting file:
if current_timepoint_number == past_timepoint_number+1 :
	my_lineage_file = selectFiles.locate_A_File(my_Parent_File_Parameters, path_to_parents)
	
else:

	#else, we search for all the parenting information between both timepoints(locateParents returns a list of files), then create the combined lineage files:
	New_Path = LineageCombine.CombineLineage(sample_number,selectFiles.locateParents(sample_number,past_timepoint,current_timepoint,path_to_parents),destination_path)
	my_lineage_file = selectFiles.locate_A_File(my_Lineage_File_Parameters,New_Path)
	
	if not my_lineage_file:
		print ("\nno lineage file found between",past_timepoint,"and",current_timepoint,"in",path_to_parents)
		sys.exit("\nEND of BackZoning")
		
print ("\nLineage file found in ", path_to_parents,":\n")
print (my_lineage_file)

#once both files are found, we can merge them:
Cell_Lineage = pd.read_csv(my_lineage_file).dropna()
Cell_Lineage= Cell_Lineage.astype(int)
Cell_Lineage.columns = ['Label_at_'+ current_timepoint ,'Label_at_'+ past_timepoint]
print (Cell_Lineage.head(10))

Zone_Position = pd.read_csv(my_zone_file).dropna()
Zone_Position= Zone_Position.astype(int)
Zone_Position.columns = ['Label_at_'+ current_timepoint ,'Zone']
print (Zone_Position.head(10))

Cell_Lineage = Cell_Lineage.merge(Zone_Position, on=Cell_Lineage.columns[0])
print ("\nMerged table:")
print (Cell_Lineage.head(10))

#we remove unwanted column here:
Cell_Lineage = Cell_Lineage.drop(columns='Label_at_'+ current_timepoint)
Cell_Lineage.columns = ['Label' ,' Parent Label']

# removal of duplicate rows in final table:
Cell_Lineage.drop_duplicates(inplace = True)

print ("\nFinal table:")
print (Cell_Lineage.head(10))

#*** NEW ***: Zone_Correction:
Cell_Lineage = Zone_Correction(my_zone_file,my_lineage_file,Cell_Lineage)

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
			
