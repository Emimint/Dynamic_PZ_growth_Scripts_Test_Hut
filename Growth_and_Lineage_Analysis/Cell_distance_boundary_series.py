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

sample_type = "LEAF" # FLOWER or LEAF
MGX_session = "/home/user/Desktop/surface_label_heatmap.mgxv"
if(sample_type == "LEAF"):
    path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/LEAF_update_viewfiles"
    sample_list = ["01","03","06","08"]
if(sample_type == "FLOWER"):
    path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/FLOWER_update_viewfiles"
    sample_list = ["01","02","19","22"]
# ========================================

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
# 	print "\nExecuting locateFile\n"
# 	print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
# 			print "Found:",my_file
# 	print "\nEnd locateFile\n"
	return my_file

def locateFiles(File_Parameters,path):
	
	my_file=""
	File_List = []
	
# 	print "\nExecuting locateFiles\n"
# 	print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
			print "Found:",my_file
			File_List.append(my_file)
# 	print "\nEnd locateFiles\n"
	
	return File_List

def Boundary_to_center_distance(mesh_file,zone_file,zone_file_viewfile, dest_dir_path):

    filename = os.path.basename(zone_file)[0:8]
    cell_dist_file = os.path.join(dest_dir_path,filename+"_boundary_to_center_distance.csv")
    heatmap_file = os.path.join(dest_dir_path,filename[0:5]+"_all_mesh_labels.csv")
    
    Process.Mesh__System__Reset('-1')
    View_Changer(MGX_session, zone_file_viewfile)
    Process.Misc__System__Load_View(MGX_session)
    Process.Mesh__System__Load(mesh_file, 'no', 'no', '0')
    Process.Mesh__Selection__Unselect()

    Process.Mesh__Heat_Map__Heat_Map_Classic('Area', 'Geometry', heatmap_file, 'Geometry', 'No', '0', '65535', 'Yes', 'No', 'None', 'No', 'Increasing', 'Ratio', '.001', '1.0')
    # identify the last one and increment it by 1:
    Csv_Info = pd.read_csv(heatmap_file, header=0).dropna()
    label_list = list(Csv_Info.Label.astype(int))
    label_list.sort() #order increasingly
    last_label=1+label_list[-1]

    boundary_label = "1"+filename[-1]
    primordium_label = filename[-1]
    APZ_label = "2"+filename[-1]
    
    #To test if boundary label exists:
    Zone_File_Info = pd.read_csv(zone_file, header=0).dropna()
    Zone_File_Info.columns = ['Label','Zone']
    Zone_File_Info['Zone'] = Zone_File_Info['Zone'].astype(int)

    zone_label_list = list(Zone_File_Info.Zone.unique())

    # Conditions to adjust boundary selection with undeterminated regions:
    Zone_File_Info.loc[(Zone_File_Info.Zone == ((int(boundary_label))+int(APZ_label))),'Zone'] = int(boundary_label)
    Zone_File_Info.loc[(Zone_File_Info.Zone == (int(boundary_label)+ int(primordium_label))),'Zone'] = int(boundary_label)    
    Zone_File_Info.loc[(Zone_File_Info.Zone == (int(boundary_label)+ int(primordium_label)+ int(APZ_label))),'Zone'] = int(boundary_label)

    Zone_File_Info['Zone'] = Zone_File_Info['Zone'].astype(str)
    zone_label_list = list(Zone_File_Info.Zone.unique())

    if(boundary_label not in zone_label_list):
        return 0

    # Save a temporary new zone_file with the modified zones:
    Zone_File_Info.columns = ['Label',' Parent Label']
    temp_zone_file = zone_file.replace(".csv","_temp.csv")
    Zone_File_Info.to_csv(temp_zone_file, index=False)
      
    Process.Mesh__Lineage_Tracking__Load_Parents(temp_zone_file, 'CSV', 'No')
    Process.Mesh__Lineage_Tracking__Select_Parents(boundary_label, 'No')
    Process.Mesh__Segmentation__Label_Selected_Vertices(last_label)
    Process.Mesh__Lineage_Tracking__Select_Parents('1000', 'No')
    Process.Mesh__Heat_Map__Measures__Location__Cell_Distance('Euclidean', 'No')
    if(sample_type == "FLOWER"):
        Process.Mesh__Heat_Map__Heat_Map_Set_Range('0', '100')
    if(sample_type == "LEAF"):
        Process.Mesh__Heat_Map__Heat_Map_Set_Range('0', '80')
    snap_title = os.path.join(dest_dir_path,cell_dist_file.replace(".csv",".png"))
    Process.Mesh__Cell_Axis__Cell_Axis_Clear()
    Process.Misc__System__Snapshot(snap_title, 'false', '0', '0', '1.0', '95')
    Process.Mesh__Heat_Map__Heat_Map_Save(cell_dist_file)
    
    Csv_Info = pd.read_csv(cell_dist_file, header=0).dropna()
    dist_val = Csv_Info.loc[Csv_Info['Label'] == last_label, 'Value'].iloc[0]

    return dist_val

Distance_Info = pd.DataFrame(columns = ['Sample_number', 'Timepoint', 'Primordium','Cell_distance'])

for sample_number in sample_list:

    file_path=os.path.join(path, sample_number,"OUTPUT")
    dest_dir_path=os.path.join(file_path, "DISTANCE_STUDY")

    for i in range(0,6):

        timepoint = "T"+str(i)
        last_label = 0


        mesh_file= locate_A_File([sample_number + "_" + timepoint],os.path.join(path, sample_number,"MESHs"))

        if not mesh_file:
            print "***No mesh not found.\n***"
            continue
        
        zone_files= locateFiles([sample_number + "_" + timepoint, "_ZONES"],os.path.join(file_path,"ZONE_PRIMORDIA"))
        zone_files.sort()
        
        for zone_file in zone_files:
            primordium = os.path.basename(zone_file)[6:8]
            zone_file_viewfile =locate_A_File([sample_number + "_" + timepoint,".mgxv"],view_file_path)
            if(zone_file_viewfile):
                cell_distance = Boundary_to_center_distance(mesh_file,zone_file,zone_file_viewfile, dest_dir_path)
                # # Add the boundary distance info for each primordium/timepoint/sample combinaison in a single dataframe:
                Distance_Info.loc[len(Distance_Info)] = [sample_number, timepoint,primordium,cell_distance]
                Distance_Info.to_csv(os.path.join(path,"All_"+sample_type +"_samples_boundary_to_center_distance_info_update.csv" ), index=False)



