#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

"""
20/02/18:

Script to automatically create growth heatmaps for a series.

"""

sample_type = "FLOWER" # FLOWER or LEAF
MGX_session = "/home/user/Desktop/session.mgxv"
if(sample_type == "LEAF"):
    destination_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    sample_list = ["01","03","06","08"]
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

for sample_number in sample_list:

    mesh_path = os.path.join(destination_path, sample_number,"MESHs")
    heatmap_path = os.path.join(destination_path, sample_number,"OUTPUT","GROWTH")
    parent_path = os.path.join(destination_path, sample_number,"OUTPUT","PARENTS")

    if os.path.exists(heatmap_path):
        print ("\nThe directory %s already exits" % (heatmap_path))
    else:
        try:
            os.mkdir(heatmap_path)
        except OSError:  
            print ("\nCreation of the directory %s failed" % (heatmap_path))
        else:  
            print ("\nSuccessfully created the directory %s " % (heatmap_path))

    for i in range(0,6):

        a = i
        timepoint = "T"+str(a)
        next_timepoint = "T"+str(a+1)

        mesh_file_Tn= locate_A_File([sample_number + "_" + timepoint, ".mgxm"],mesh_path)
        mesh_file_Tn_1= locate_A_File([sample_number + "_" + next_timepoint, ".mgxm"],mesh_path)
        parent_file =locate_A_File([sample_number+"_PARENTS_"+timepoint,".csv"],parent_path)

        if(mesh_file_Tn and parent_file and mesh_file_Tn_1):                 
            Process.Misc__System__Load_View(MGX_session)                   
            Process.Mesh__System__Load(mesh_file_Tn_1, 'no', 'no', '0')
            Process.Mesh__Selection__Unselect()
            Process.Mesh__Lineage_Tracking__Load_Parents(parent_file, 'CSV', 'No')
            Process.Mesh__System__Save(mesh_file_Tn_1, 'No', '0')
            Process.Mesh__MultiMesh__Swap_or_Copy_Mesh_1_and_2('1 -> 2')
            Process.Mesh__System__Load(mesh_file_Tn, 'no', 'no', '0')
            Process.Mesh__Selection__Unselect()
            outfile = os.path.join(heatmap_path, sample_number +"_"+timepoint+next_timepoint+"_GROWTH.csv")
            Process.Mesh__Heat_Map__Heat_Map_Classic('Area', 'Geometry', outfile, 'Geometry', 'No', '0', '65535', 'Yes', 'No', 'None', 'Yes', 'Increasing', 'Ratio', '.001', '1.0')
 
