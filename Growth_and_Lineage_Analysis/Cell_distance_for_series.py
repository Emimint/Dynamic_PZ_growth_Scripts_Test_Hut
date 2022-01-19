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
MGX_session = "/home/user/Desktop/surface_label_heatmap.mgxv"
if(sample_type == "LEAF"):
    path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/LEAF_update_viewfiles"
    sample_list = ["01","03","06","08"]
if(sample_type == "FLOWER"):
    path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/FLOWER_update_viewfiles"
    sample_list = ["01","02","19","22"]

# ========================================

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
# 			print "Found:",my_file
			File_List.append(my_file)
# 	print "\nEnd locateFiles\n"
	
	return File_List

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

def Cell_distance(mesh_file,zone_file,dest_dir_path):

    filename = os.path.basename(zone_file)[0:5]
    cell_dist_file = os.path.join(dest_dir_path,filename+"_cell_distance.csv")
    snap_title = os.path.join(dest_dir_path,filename+"_cell_distance.png")
    
    Process.Mesh__System__Reset('-1')
    zone_file_viewfile =locate_A_File([filename[0:5],".mgxv"],view_file_path)

    if(zone_file_viewfile):
        View_Changer(MGX_session, zone_file_viewfile)    
        Process.Misc__System__Load_View(MGX_session)
        Process.Mesh__System__Load(mesh_file, 'no', 'no', '0')
        Process.Mesh__Selection__Unselect()
        Process.Mesh__Lineage_Tracking__Load_Parents(zone_file, 'CSV', 'No')
        Process.Mesh__Lineage_Tracking__Select_Parents('1000', 'No')
        Process.Mesh__Heat_Map__Measures__Location__Cell_Distance('Euclidean', 'No')
        Process.Mesh__Heat_Map__Heat_Map_Save(cell_dist_file)
        Process.Mesh__Selection__Unselect()
        Process.Mesh__Cell_Axis__Cell_Axis_Clear()
        if(sample_type == "FLOWER"):
            Process.Mesh__Heat_Map__Heat_Map_Set_Range('0', '100')
        if(sample_type == "LEAF"):
            Process.Mesh__Heat_Map__Heat_Map_Set_Range('0', '80')
        Process.Misc__System__Snapshot(snap_title, 'false', '0', '0', '1.0', '95')


# # # # # MAIN # # # # # :
# =========================

for sample_number in sample_list:

    file_path=os.path.join(path, sample_number,"OUTPUT")
    zone_file_path=os.path.join(file_path, "MERISTEM_ZONES")
    dest_dir_path=os.path.join(file_path, "DISTANCE_STUDY")

    for i in range(0,6):

        timepoint = "T"+str(i)

        mesh_file= locate_A_File([sample_number + "_" + timepoint],os.path.join(path, sample_number,"MESHs"))

        if not mesh_file:
            print "***No mesh not found.\n***"
            continue
        
        zone_file =locate_A_File([sample_number + "_" + timepoint + "_all_Meristem_zones.csv"],zone_file_path)

        if zone_file:
            Cell_distance(mesh_file,zone_file,dest_dir_path)
