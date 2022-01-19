#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
import os
import datetime
import re

"""
20/02/18:

Script to automatically snap a .png of a list of files.

YOU MUST FIRST make a screenshot in MGX manually for this to work, using the Misc__System__Snapshot option.

"""

sample_type = "FLOWER" # FLOWER or LEAF
MGX_session_A = "/home/user/Desktop/surface_parents_color_change_A.mgxv"
MGX_session_B = "/home/user/Desktop/surface_parents_color_change_B.mgxv"
if(sample_type == "LEAF"):
    destination_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    sample_list = ["01","03","06","08"]
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/LEAF_update_viewfiles"
if(sample_type == "FLOWER"):
    destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    sample_list = ["01","02","19","22"]
    view_file_path = "/home/user/Desktop/Project_2/MGX_processing_files/FLOWER_update_viewfiles"
# # # ===================================
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

def locateFiles(File_Parameters,path):
	
	my_file=""
	File_List = []
	
	print "\nExecuting locateFiles\n"
	print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
			print "Found:",my_file
			File_List.append(my_file)
	print "\nEnd locateFiles\n"
	
	return File_List

mylist=[]
today = datetime.date.today()
mylist.append(today)

for sample_number in sample_list:

    mesh_path = os.path.join(destination_path, sample_number,"MESHs")
    heatmap_path = os.path.join(destination_path, sample_number,"OUTPUT","ZONE_PRIMORDIA")

    #creation du repertoire contenant l'output de Screenshoot_maker:
    timestamp = str(mylist[0]) .replace("-", "_") 
    New_Directory = timestamp+"_"+"ZONES_SNAPSHOTs"
    path_to_New_Directory = os.path.join(heatmap_path,New_Directory)

    print path_to_New_Directory
    print heatmap_path

    if os.path.exists(path_to_New_Directory):
        print ("\nThe directory %s already exits" % (New_Directory))
    else:
        try:
            os.mkdir(path_to_New_Directory)
        except OSError:  
            print ("\nCreation of the directory %s failed" % (New_Directory))
            exit()
        else:  
            print ("\nSuccessfully created the directory %s " % (New_Directory))

    for filename in os.listdir(mesh_path):

        file = os.path.join(mesh_path,filename)
        print file
        
        if filename.endswith(".mgxm"):
            zone_file_list =locateFiles([filename[0:5], "_ZONES.csv"],heatmap_path)
            print zone_file_list
            for zone_file in zone_file_list:
                # Process.Mesh__System__Reset('-1')
                print zone_file
                print zone_file[-11:-10]
                zone_file_viewfile =locate_A_File([filename[0:5],".mgxv"],view_file_path)
                print zone_file_viewfile
                if(zone_file_viewfile):
                    if((zone_file[-11:-10]) in ["1","3","4"]):
                        View_Changer(MGX_session_A, zone_file_viewfile)
                        Process.Misc__System__Load_View(MGX_session_A)
                    else:
                        View_Changer(MGX_session_B, zone_file_viewfile)
                        Process.Misc__System__Load_View(MGX_session_B)              
                    Process.Mesh__System__Load(file, 'no', 'no', '0')
                    Process.Mesh__Selection__Unselect()
                    Process.Mesh__Cell_Axis__Cell_Axis_Clear()
                    Process.Mesh__Lineage_Tracking__Load_Parents(zone_file, 'CSV', 'No')
                    snap_title = os.path.join(path_to_New_Directory,os.path.basename(zone_file.replace(".csv","_snap.png")))
                    print snap_title
                    Process.Misc__System__Snapshot(snap_title, 'false', '0', '0', '1.0', '95')

