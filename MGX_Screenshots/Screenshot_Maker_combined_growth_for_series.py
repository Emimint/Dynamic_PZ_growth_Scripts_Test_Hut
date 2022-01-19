#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

"""

Script to automatically snap a .png of meshes showing combined lineage.
YOU MUST FIRST make a screenshot in MGX manually for this to work, using the Misc__System__Snapshot option.
View_Changer is called to change the zoom and orientation of the sample. 

"""
sample_type = "LEAF" # FLOWER or LEAF
MGX_session = "/home/user/Desktop/surface_label_heatmap_no_mesh.mgxv"
if(sample_type == "LEAF"):
    destination_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/LEAF_update_viewfiles"
    sample_list = ["01","03","06","08"]
if(sample_type == "FLOWER"):
    destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE"# path to LEAF or FLOWER DATA
    view_file_path = "/home/user/Desktop/Project_2/FLOWER_update_viewfiles"
    sample_list = ["01","02","19","22"]
# # # ===================================

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

	return my_file

def locateFiles(File_Parameters,path):
	
	my_file=""
	File_List = []
	
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
			File_List.append(my_file)
	
	return File_List

mylist=[]
today = datetime.date.today()
mylist.append(today)

for sample_number in sample_list:

    cell_lineage_start = ""
    cell_lineage_end = ""

    mesh_path = os.path.join(destination_path, sample_number,"MESHs")
    heatmap_path = os.path.join(destination_path, sample_number,"OUTPUT","LINEAGE_COMBINE")

    if os.path.exists(heatmap_path):
        print ("\nThe directory %s already exits" % (heatmap_path))
    else:
        try:
            os.mkdir(heatmap_path)
        except OSError:  
            print ("\nCreation of the directory %s failed" % (heatmap_path))
        else:  
            print ("\nSuccessfully created the directory %s " % (heatmap_path))

    file_list = os.listdir(mesh_path)
    file_list.sort()

    for file in file_list:
        if("_T0" in file):
            cell_lineage_start = file
        if("_T3" in file):
            cell_lineage_end = file
        if("_T4" in file):
            cell_lineage_end = file

    Process.Mesh__System__Load(os.path.join(mesh_path,cell_lineage_start), 'no', 'no', '0')
    Process.Mesh__System__Load(os.path.join(mesh_path,cell_lineage_end), 'no', 'no', '0')
    file_viewfile =locate_A_File([cell_lineage_start[0:5],".mgxv"],view_file_path)
    lineage_file =locate_A_File([cell_lineage_start[0:5],"_ZONES.csv"],heatmap_path)

    if(file_viewfile and lineage_file):
        View_Changer(MGX_session, file_viewfile)                  
        Process.Misc__System__Load_View(MGX_session)                   
        Process.Mesh__System__Load(file, 'no', 'no', '0')
        Process.Mesh__Selection__Unselect()
        Process.Mesh__Lineage_Tracking__Load_Parents(lineage_file, 'CSV', 'No')
        Process.Mesh__Heat_Map__Delete_Heat_Range_Labels('Yes', 'No', '', '')
        Process.Mesh__Heat_Map__Delete_Heat_Range_Labels('Yes', 'No', '', '')
        Process.Mesh__Heat_Map__Heat_Map_Classic('Area', 'Geometry', '', 'Geometry', 'No', '0', '65535', 'Yes', 'No', 'None', 'No', 'Increasing', 'Ratio', '.001', '1.0')

        Process.Mesh__Cell_Axis__Cell_Axis_Clear()
        Process.Mesh__System__Reset('1')
        snap_title = os.path.join(heatmap_path,filename[0:5]+"_combined_growth_snap.png")
        Process.Misc__System__Snapshot(snap_title, 'false', '0', '0', '1.0', '95')

