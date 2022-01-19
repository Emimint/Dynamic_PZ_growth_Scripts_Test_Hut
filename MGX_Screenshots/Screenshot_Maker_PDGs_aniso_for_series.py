#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
import os
import datetime
import re
import fileinput
import pandas as pd
import numpy as np

"""
20/02/18:

Script to automatically snap a .png of a list of files.

YOU MUST FIRST make a screenshot in MGX manually for this to work, using the Misc__System__Snapshot option.
About MGX_session_A and MGX_session_B: viewfile made with color pattern from Primordia_zone_color_code_combinaison_A/B.mgx.labels (as defined in /home/user/Desktop/Project_2/Zone_prediction_color_coding.ods).

    21/08/25:
    
    - view_file_modifier is called to change the zoom and orientation of the sample. 


"""

sample_type = "FLOWER" # FLOWER or LEAF
MGX_session = "/home/user/Desktop/surface_label_heatmap_no_mesh.mgxv"
if(sample_type == "LEAF"):
    destination_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/LEAF_update_viewfiles"
    sample_list = ["01","03","06","08"]
if(sample_type == "FLOWER"):
    destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/FLOWER_update_viewfiles"
    sample_list = ["01","02","19","22"]
# # # ===================================
Param_Values = dict(zip(['Min', 'Max','Aniso'], ['1', '2','3']))

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
	
# 	print "\nExecuting locateFiles\n"
# 	print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
# 			print "Found:",my_file
			File_List.append(my_file)
# 	print "\nEnd locateFiles\n"
	
	return File_List


for param in ['Min', 'Max','Aniso']:
    for sample_number in sample_list:

        mesh_path = os.path.join(destination_path, sample_number,"MESHs")
        heatmap_path = os.path.join(destination_path, sample_number,"OUTPUT","PDGs_ANISOTROPY","MEANs")

        if os.path.exists(heatmap_path):
            print ("\nThe directory %s already exits" % (heatmap_path))
        else:
            try:
                os.mkdir(heatmap_path)
            except OSError:  
                print ("\nCreation of the directory %s failed" % (heatmap_path))
            else:  
                print ("\nSuccessfully created the directory %s " % (heatmap_path))

        for filename in os.listdir(mesh_path):

            file = os.path.join(mesh_path,filename) 
            print file
            
            if filename.endswith(".mgxm"):
                    timepoint = filename.split('_')[1]
                    file_viewfile =locate_A_File([filename[0:5],".mgxv"],view_file_path)
                    mean_val_file_list =locateFiles(['_'+ timepoint +'_',".csv"],heatmap_path)
                    print file_viewfile
                    print mean_val_file_list
                    for mean_val_file in mean_val_file_list:
                        primordium = os.path.basename(mean_val_file).split('_')[2]
                        if(file_viewfile and mean_val_file):
                            View_Changer(MGX_session, file_viewfile)
                            Process.Misc__System__Load_View(MGX_session)     
                            Process.Mesh__System__Load(file, 'no', 'no', '0')
                            Process.Mesh__Selection__Unselect()
                            Process.Mesh__Heat_Map__Delete_Heat_Range_Labels('Yes', 'No', '', '')
                            Process.Mesh__Heat_Map__Delete_Heat_Range_Labels('Yes', 'No', '', '')
                            print mean_val_file
                            Mean_Val_File = pd.read_csv(mean_val_file).dropna()
                            list_of_values = list(Mean_Val_File['Min_x'].unique())
                            print "list_of_values", list_of_values
                            if(len(list_of_values) > 1 ):
                                Process.Mesh__Heat_Map__Heat_Map_Load(mean_val_file, Param_Values[param], '1.0')
                                if(param == "Aniso"):
                                    Process.Mesh__Heat_Map__Heat_Map_Set_Range('45', '300')
                                if(param in ["Min","Max"]):
                                    Process.Mesh__Heat_Map__Heat_Map_Set_Range('-30', '60')
                                Process.Mesh__Cell_Axis__Cell_Axis_Clear()
                                snap_title = os.path.join(heatmap_path,filename[0:5]+"_"+primordium+"_mean_"+param+"_PDG_snap.png")
                                print snap_title
                                Process.Misc__System__Snapshot(snap_title, 'false', '0', '0', '1.0', '95')

