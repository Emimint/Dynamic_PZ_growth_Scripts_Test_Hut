#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import time
from datetime import datetime
import os
import os.path
import csv
import pandas as pd
import numpy as np
import math

sample_type = "FLOWER" # FLOWER or LEAF
MGX_session = '/home/user/Desktop/surface_label_heatmap.mgxv' # for surface and heatmaps
if(sample_type == "LEAF"):
    path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/LEAF_update_viewfiles"
    sample_list = ["01","03","06","08"]
if(sample_type == "FLOWER"):
    path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/FLOWER_update_viewfiles"
    sample_list = ["01","02","19","22"]
# ========================================

Zone_Dict = {"APZ": "2","boundary": "1","primordium": ""}

def View_Changer(input_viewfile, dict_viewfile):
 
    cues = ['CameraFrame','SceneRadius','CameraZoom']
    new_lines = []
    
    
    # Collect the lines that need to be changed:
    file = open(dict_viewfile, "r")

    for line in file:
        changes = line
        line = line.strip()
        for i in cues:
            if(line.startswith(i)):
                new_lines.append(line+"\n")
    file.close()

    new_parameters =dict(zip(cues,new_lines))


    # Make the changes in a copy:
    my_file = open(input_viewfile, "r")
    replacement = ""
    original = ""

    for line in my_file:
        no_changes = line
        changes = line
        line = line.strip()
        for i in ['CameraFrame','SceneRadius','CameraZoom']:
            if(line.startswith(i)):
                changes = line.replace(line, new_parameters[i])
        replacement = replacement + changes
        original = original + no_changes
    my_file.close()

    # Save the modified viewfile:
    file_out = open(input_viewfile, "w")
    file_out.write(replacement)
    file_out.close()

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

def locateFiles(File_Parameters,path):
	
	my_file=""
	File_List = []
	
	# print "\nExecuting locateFiles\n"
	# print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
			# print "Found:",my_file
			File_List.append(my_file)
	# print "\nEnd locateFiles\n"
	
	return File_List

def Simplified_Zone(zone_file):
    # Fonction to automatically give a boundary label to unspecified cells:

    filename = os.path.basename(zone_file)[0:8]
    
    #To test if boundary label exists:
    Zone_File_Info = pd.read_csv(zone_file, header=0).dropna()
    Zone_File_Info.columns = ['Label','Zone']
    Zone_File_Info = Zone_File_Info[Zone_File_Info.Zone != 0]
    Zone_File_Info['Zone'] = Zone_File_Info['Zone'].astype(int)

    # Conditions to adjust boundary selection with undeterminated regions:
    Zone_File_Info.loc[(Zone_File_Info.Zone == ((int(boundary_label))+int(APZ_label))),'Zone'] = int(boundary_label)
    Zone_File_Info.loc[(Zone_File_Info.Zone == (int(boundary_label)+ int(primordium_label))),'Zone'] = int(boundary_label)    
    Zone_File_Info.loc[(Zone_File_Info.Zone == (int(boundary_label)+ int(primordium_label)+ int(APZ_label))),'Zone'] = int(boundary_label)

    Zone_File_Info['Zone'] = Zone_File_Info['Zone'].astype(str)
    
    # print "Zone_File_Info"
    # print Zone_File_Info
    
    return Zone_File_Info

def Size_calculator(primordium, mesh_file,Zone_File,dest_dir_path):

    filename = os.path.basename(mesh_file)[0:5] +"_"+primordium
    Zone_File.to_csv(os.path.join(dest_dir_path,filename +"_"+timepoint+next_timepoint+"_zone.csv"), index=False)
    zone_file = os.path.join(dest_dir_path,filename +"_"+timepoint+next_timepoint+"_zone.csv")
    print ("*******")
    print ("in Size_calculator ")
    print("filename",filename)
    print ("input dataframe ")
    print (Zone_File.head(1))
    print ("input dataframe corresponding csv",zone_file)


    zone_size_file = zone_file.replace("_zone.csv","_zone_size_info_temp.csv")
    print ("heatmap file for zones ", zone_size_file)

    Process.Mesh__System__Reset('-1')
    file_viewfile =locate_A_File([filename[0:5],".mgxv"],view_file_path)
    View_Changer(MGX_session, file_viewfile)
    Process.Misc__System__Load_View(MGX_session)
    Process.Mesh__System__Load(mesh_file, 'no', 'no', '0')
    Process.Mesh__Selection__Unselect()      
    Process.Mesh__Lineage_Tracking__Load_Parents(zone_file, 'CSV', 'No')
    Process.Mesh__Lineage_Tracking__Copy_Parents_to_Labels()
    Process.Mesh__Heat_Map__Heat_Map_Classic('Area', 'Geometry', zone_size_file, 'Geometry', 'No', '0', '65535', 'Yes', 'No', 'None', 'No', 'Increasing', 'Ratio', '.001', '1.0')
    snap_title = zone_file.replace(".csv",".png")
    Process.Misc__System__Snapshot(snap_title, 'false', '0', '0', '1.0', '95')

    Csv_Info = pd.read_csv(zone_size_file, usecols=[0,1], header=0).dropna()
    Csv_Info['Label'] = Csv_Info['Label'].astype(str)
    
    Csv_Info.loc[(Csv_Info.Label == APZ_label),'Label'] = "APZ"
    Csv_Info.loc[(Csv_Info.Label == primordium_label),'Label'] = "primordium"    
    Csv_Info.loc[(Csv_Info.Label == boundary_label),'Label'] = "boundary"


    print "Csv_Info"
    print Csv_Info
    print ("out Size_calculator ")
    print ("*******")
    
    return Csv_Info

# # # MAIN # # #:

Cell_Size_Info = pd.DataFrame(columns = ['Sample_number', 'Timepoint', 'Primordium','Zone', 'total_size_Tn',  'total_size_Tn_1', 'Growth'])

for sample_number in sample_list:

    file_path=os.path.join(path, sample_number,"OUTPUT")
    dest_dir_path=os.path.join(file_path, "ZONE_PRIMORDIA")

    for i in range(0,6):

        a = i
        timepoint = "T"+str(a)
        next_timepoint = "T"+str(a+1)

        mesh_file_Tn= locate_A_File([sample_number + "_" + timepoint],os.path.join(path, sample_number,"MESHs"))
        mesh_file_Tn_1= locate_A_File([sample_number + "_" + next_timepoint],os.path.join(path, sample_number,"MESHs"))

        if not mesh_file_Tn_1:
            print ("***No more mesh not found.\n***")
            continue
        
        zone_files= locateFiles([sample_number + "_" + timepoint, "_ZONES.csv"],os.path.join(file_path,"ZONE_PRIMORDIA"))
        zone_files.sort()

        parent_file= locate_A_File([sample_number + "_PARENTS_" + timepoint, ".csv"],os.path.join(file_path,"PARENTS"))
        if (parent_file):
            Parent_Label_List = pd.read_csv(parent_file, header=0).dropna()
            Parent_Label_List.columns = ['Label','Parent_label']
            # Parent_Label_List.columns = ['Label_at'+next_timepoint,'Label_at'+timepoint]
        else:
            continue

        for original_zone_file in zone_files:

            primordium = os.path.basename(original_zone_file)[6:8]
        
            primordium_number = primordium[-1]

            boundary_label = "1"+ primordium_number
            primordium_label = primordium_number
            APZ_label = "2"+ primordium_number

            
            if(parent_file):

                # # correct zone selection:
                Zone_Label_List = Simplified_Zone(original_zone_file)
                Zone_Label_List.columns = ['Parent_label','Zone']
                Fixed_List = Zone_Label_List.merge(Parent_Label_List, on=['Parent_label'])

                # # Fixed list on Tn:
                First_List = Fixed_List.drop('Label', axis = 1).drop_duplicates()
                First_List.columns = ['Label','Parent_label']

                # # Fixed list on Tn+1:
                Second_List = Fixed_List.drop('Parent_label', axis = 1).drop_duplicates()
                Second_List = Second_List.reindex(columns=['Label','Zone'])
                Second_List.columns = ['Label',' Parent_label']
            
            if(First_List.empty == False and Second_List.empty == False):
                Table_Zone_Size_Tn = Size_calculator(primordium, mesh_file_Tn, First_List,dest_dir_path)
                
                print ("Data for file 1")
                print ("===============")
                print ("timepoint ",timepoint)
                print ("next_timepoint ",next_timepoint)
                print ("primordium ",primordium)
                print ("Fixed_List ")
                print (Fixed_List.head(1))
                print ("First_List ")
                print (First_List.head(1))
                print ("mesh_file_Tn ",mesh_file_Tn)
                print ("original_zone_file ",original_zone_file)
                print ("parent_file ",parent_file)

                Table_Zone_Size_Tn.columns = ['Label','Size_Tn']
                Table_Zone_Size_Tn_1 = Size_calculator(primordium, mesh_file_Tn_1, Second_List,dest_dir_path)
                print ("    ")
                print ("Data for file 2")
                print ("===============")
                print ("timepoint ",timepoint)
                print ("next_timepoint ",next_timepoint)
                print ("primordium ",primordium)
                print ("Second_List ")
                print (Second_List.head(1))
                print ("mesh_file_Tn_1 ",mesh_file_Tn_1)
                print ("original_zone_file ",original_zone_file)
                print ("parent_file ",parent_file)

                Table_Zone_Size_Tn_1.columns = ['Label','Size_Tn_1']
                Table_Zone_Size_Tn = Table_Zone_Size_Tn.merge(Table_Zone_Size_Tn_1,on=['Label'])
                print ("Table_Zone_Size_Tn")
                print (Table_Zone_Size_Tn  )
                print ("Table_Zone_Size_Tn_1")
                print (Table_Zone_Size_Tn_1 )                
                Table_Zone_Size_Tn['Growth'] = (Table_Zone_Size_Tn['Size_Tn_1']/Table_Zone_Size_Tn['Size_Tn'])

                for index, row in Table_Zone_Size_Tn.iterrows():
                    # Add the zone size info for each primordium/timepoint/sample combinaison in a single dataframe:
                    Cell_Size_Info.loc[len(Cell_Size_Info)] = [sample_number, timepoint,primordium]+ list(row)
                print "Cell_Size_Info"
                print Cell_Size_Info
                Cell_Size_Info.to_csv(os.path.join(path,"ALL_"+sample_type +"_samples_all_zones_info.csv" ), index=False)
                del First_List, Second_List, Zone_Label_List 
                print ("///////////")



