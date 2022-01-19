#/usr/bin/Python 3.8.8
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import os
import os.path
import pandas as pd
import selectFiles # on choisit, en fonction des timepoints et des parametres choisis, les fichiers necessaires.
import LineageCombine

"""

	19/05/05: 
	Script done under Python 2.7.12.

	ForwardZoning is a method to assign zones at a future timepoint using a past timepoint zone information. It is based on the BackZoning script.
	
	See BackZoning script for more info.
    
    21/08/03:
    
    - Final file can be saved in a new folder or in same location as zone info file. 
	
"""
my_lineage_file=""
sample_number = "02"
current_timepoint_number = 3 # indicate the number of the timepoint with your zones.
future_timepoint_number = 4 # indicate the timepoint of interest.
search_str = "_P4_ZONES" # str used for search of the zone file.
path_to_zone = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/02/OUTPUT/ZONE_PRIMORDIA"
path_to_parents = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/02/OUTPUT/PARENTS"
# path_to_backzoning_file = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/08/OUTPUT/ZONE_PRIMORDIA" # if needed, indicate zone file (Regular zone file or BackZoning file) location
destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/02/OUTPUT"
saving_option = "new_zone_folder" # Choose "in_zone_folder" or "new_zone_folder" : final file will be saved either in a new directory ("in_zone" option) or in the same folder as the zone file ("zone_folder" option).
option = "1" # 1 to ignore previous zone information; 2 otherwise.
# # ====================================================



# liste of parametres for future file search:
current_timepoint = "T"+ str(current_timepoint_number)
future_timepoint = "T"+ str(future_timepoint_number)

# liste of parametres for future file searches (fill manually):
# my_Zone_Parameters = [sample_number,current_timepoint,"_central_cell",".csv"]
my_Zone_Parameters = [sample_number,current_timepoint,search_str,".csv"]
my_Parent_File_Parameters = [sample_number,current_timepoint+future_timepoint,"PARENTS",".csv"]
my_Lineage_File_Parameters = [sample_number,current_timepoint+future_timepoint,"_LineageCombine_",".csv"]
My_Backzoning_File_Parameters = [sample_number+"_BackZoning_"+current_timepoint+future_timepoint+".csv"]

if (option == "2"):
    My_Backzoning_File_Parameters = [sample_number+"_"+future_timepoint , search_str]

#First, we are looking for the zone file with at the requested timepoint:
my_zone_file = selectFiles.locate_A_File(my_Zone_Parameters, path_to_zone)

if not my_zone_file:
	print("\nNo zone file zone found at",current_timepoint,"in",path_to_zone)
	sys.exit("\nEND of ForwardZoning")

#Then, if the timepoints are consecutive, look for original parenting file:
if current_timepoint_number == (future_timepoint_number-1) :
	my_lineage_file = selectFiles.locate_A_File(my_Parent_File_Parameters, path_to_parents)
else:
	#else, we search for all the parenting information between both timepoints(locateParents returns a list of files), then create the combined lineage files:
    New_Path = LineageCombine.CombineLineage(sample_number,selectFiles.locateParents(sample_number,current_timepoint,future_timepoint,path_to_parents),destination_path)
    my_lineage_file = selectFiles.locate_A_File(my_Lineage_File_Parameters,New_Path)
	
    if not my_lineage_file:
        print("\nno lineage file found between",current_timepoint,"and",future_timepoint,"in",path_to_parents)
        sys.exit("\nEND of ForwardZoning")
		
print("\nLineage file found in ", path_to_parents,":\n")
print(my_lineage_file)

#once both files are found, we can merge them:
Cell_Lineage = pd.read_csv(my_lineage_file).dropna() 
Cell_Lineage.columns = ['Label_at_'+ future_timepoint ,'Label_at_'+ current_timepoint]
print(Cell_Lineage.head(10))
Zone_Position = pd.read_csv(my_zone_file).dropna()  
Zone_Position.columns = ['Label_at_'+ current_timepoint ,'Zone']
print(Zone_Position.head(10))

Cell_Lineage = Cell_Lineage.merge(Zone_Position, on=Cell_Lineage.columns[1])
print("\nMerged table:")
print(Cell_Lineage.head(10))
#we remove unwanted column here:
Cell_Lineage = Cell_Lineage.drop(columns='Label_at_'+ current_timepoint)
print("\nCell_Lineage table:")
print(Cell_Lineage.head(10))

# /!\/!\/!\/!\ Un-comment as needed, pick your option /!\/!\/!\/!\:
# OPTION 1): We do not needed the previous zone information:
if (option == "1"):
    Final_Cell_Lineage = Cell_Lineage

# OPTION 2) We want to keep the old zone information:
if (option == "2"):

    # we open the corresponding BackZoning_file:
    my_backzoning_file = selectFiles.locate_A_File(My_Backzoning_File_Parameters, path_to_backzoning_file)

    if not my_backzoning_file:
        print(" no backzoning file found between ",current_timepoint," and ",future_timepoint," in ",path_to_parents)
        sys.exit(" END of ForwardZoning")

    print("my_backzoning_file file found in " + path_to_backzoning_file +" :")
    print(my_backzoning_file)

    Cell_Lineage_From_Backzoning = pd.read_csv(my_backzoning_file).dropna() 
    Cell_Lineage_From_Backzoning.columns = ['Label_at_'+ future_timepoint ,'Zone']
    print(" Cell_Lineage_From_Backzoning table:")
    print(Cell_Lineage_From_Backzoning.head(10))
    print(Cell_Lineage.head(10))
    Final_Cell_Lineage = pd.concat([Cell_Lineage_From_Backzoning, Cell_Lineage],axis = 0, ignore_index=False)
    # Final_Cell_Lineage = pd.concat([Cell_Lineage, Cell_Lineage_From_Backzoning],axis = 0, ignore_index=False)
    #END OF OPTION 2.

# important to remove identical labels (if any) from the final file:
Final_Cell_Lineage.columns = ['Label' ,' Parent Label']
Final_Cell_Lineage.drop_duplicates(subset = ['Label'], keep='last',inplace=True)
print("\nFinal_Cell_Lineage:")
print(Final_Cell_Lineage)
print(Final_Cell_Lineage.head(10))


if(saving_option == "new_zone_folder"):
    #creation of the ForwardZoning output directory:
    timestamp = str(datetime.now().date()).replace("-","")[2:]
    New_Directory = timestamp+"_FORWARDZONING_RESULTS"
    path_to_New_Directory = os.path.join(destination_path,New_Directory)

    if os.path.exists(path_to_New_Directory):
        print("\nThe directory %s already exits in %s" % (New_Directory,destination_path))
    else:
        try:
            os.mkdir(path_to_New_Directory)
        except OSError:  
            print("\nCreation of the directory %s failed" % New_Directory)
            exit()
        else:  
            print("\nSuccessfully created the directory %s in %s " % (New_Directory,destination_path))
        
    #the resulting ForwardZoning information is then converted in .csv for use in MGX:
    selectFiles.DataFrameToCsv(Final_Cell_Lineage , sample_number + "_ForwardZoning_" + current_timepoint +  future_timepoint + ".csv",path_to_New_Directory)

if(saving_option == "in_zone_folder"):
    Final_Cell_Lineage.to_csv(my_zone_file.replace(current_timepoint,future_timepoint), index=False)


