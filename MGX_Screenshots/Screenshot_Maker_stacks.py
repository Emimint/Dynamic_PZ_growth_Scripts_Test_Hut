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
sample_number = "22"
MGX_session = "/home/user/Desktop/stack_only.mgxv"
stack_path = "/media/user/BACKUP/Emilie/210505_PROJECT_DATA/FLOWER_DATA/2020128_102_PM_YFP_rep_SAM_22"

if(sample_type == "LEAF"):
    destination_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/LEAF_update_viewfiles"

if(sample_type == "FLOWER"):
    destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/FLOWER_update_viewfiles"

# # # ===================================

mylist=[]
today = datetime.date.today()
mylist.append(today)
dir_path = os.path.join(destination_path, sample_number,"OUTPUT","STACKs_SNAPs")

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
	print "\nExecuting locateFile\n"
	print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
			print "Found:",my_file
	print "\nEnd locateFile\n"
	return my_file

print dir_path
if os.path.exists(dir_path):
	print ("\nThe directory %s already exits" % (dir_path))
else:
	try:
		os.mkdir(dir_path)
	except OSError:  
		print ("\nCreation of the directory %s failed" % (dir_path))
		exit()
	else:  
		print ("\nSuccessfully created the directory %s " % (dir_path))

for filename in os.listdir(stack_path):
    file = os.path.join(stack_path,filename)
    print filename
    print file

    if filename.endswith(".czi._trimmed_ome.tif"):
        print filename
        # /!\/!\/!\/!\ check original .tif name /!\/!\/!\/!\:
        snap_title = os.path.join(dir_path,filename.replace(".czi._trimmed_ome.tif","_stack_snap.png"))
        print snap_title
        file_viewfile =locate_A_File([filename[0:5],".mgxv"],view_file_path)
        if(file_viewfile):
            View_Changer(MGX_session, file_viewfile)                  
            Process.Misc__System__Load_View(MGX_session)
            Process.Stack__System__Open(file, 'Main', '0', '')
            Process.Misc__System__Snapshot(snap_title, 'false', '0', '0', '1.0', '95')
