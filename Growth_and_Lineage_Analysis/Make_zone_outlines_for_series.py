#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import sys
import os
import datetime
import re
import fileinput

"""
20/02/18:

Script to automatically create proli heatmaps for a series.

/!\ You MUST first make sure the parents are already saved on the meshes! (Tip: Use Make_Growth_for_series.py first) /!\

"""

sample_type = "LEAF" # FLOWER or LEAF
if(sample_type == "LEAF"):
    destination_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    # sample_list = ["01","03","06","08"]
    sample_list = ["03"]
if(sample_type == "FLOWER"):
    destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    sample_list = ["01","02","19","22"]
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

for sample_number in sample_list:

    mesh_path = os.path.join(destination_path, sample_number,"MESHs")
    outline_path = os.path.join(destination_path, sample_number,"MESHs","OUTLINE_ZONE_MESHs")
    zone_path = os.path.join(destination_path, sample_number,"OUTPUT","ZONE_PRIMORDIA","SIZE_ANALYSIS_CONTROL_FILES")

    if os.path.exists(outline_path):
        print ("\nThe directory %s already exits" % (outline_path))
    else:
        try:
            os.mkdir(outline_path)
        except OSError:  
            print ("\nCreation of the directory %s failed" % (outline_path))
        else:  
            print ("\nSuccessfully created the directory %s " % (outline_path))


    for i in range(0,6):

        a = i
        timepoint = "T"+str(a)
        next_timepoint = "T"+str(a+1)
        filestart = sample_number + "_" + timepoint
        mesh_file= locate_A_File([filestart, ".mgxm"],mesh_path)
        
        if (mesh_file):
            zone_file_list =locateFiles([filestart+"_P", timepoint + next_timepoint +"_zone.csv"],zone_path)
            zone_file_list.sort()

            for zone_file in zone_file_list:
                primordium = os.path.basename(zone_file)[6:8]
                outfile = os.path.join(outline_path,filestart +"_"+primordium+".mgxm")
                Process.Mesh__System__Load(mesh_file, 'no', 'no', '0')
                Process.Mesh__Lineage_Tracking__Load_Parents(zone_file, 'CSV', 'No')
                Process.Mesh__Lineage_Tracking__Copy_Parents_to_Labels()
                Process.Mesh__Selection__Select_Labeled('No')
                Process.Mesh__System__Save(outfile, 'No', '0')

