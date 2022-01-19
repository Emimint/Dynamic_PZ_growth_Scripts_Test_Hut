#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import pandas as pd


"""
Script to generate masterfile, with all cell information.

"""
sample_type = "LEAF"# LEAF or FLOWER 
if(sample_type == "LEAF"):
    path = "C:/Users/bell1/Downloads/PROJECT_02_MERISTEM_DYNAMICS/PROJECT_02_MERISTEM_DYNAMICS/210809_LEAF_DATA_EE"
    sample_list = ["01","03","06","08"]
    # sample_list = ["01"]
if(sample_type == "FLOWER"):
    path = "C:/Users/bell1/Downloads/PROJECT_02_MERISTEM_DYNAMICS/PROJECT_02_MERISTEM_DYNAMICS/210623_FLOWER_DATA_EE"
    sample_list = ["01","02","19","22"]
day_or_night = "all"; # day_formed_primordia, night_formed_primordia or all (samples)
output = 'C:/Users/bell1/Desktop/test'
outfilename = sample_type+"_all_cell_info_"+day_or_night+"_samples_all_zones_masterfile.csv"
# ========================================
filter_dict = dict(zip(["day_formed_primordia","night_formed_primordia"],[1,0]))
Zone_Dict = {"PZ": 1111,"center": 1000,"CZ": 666}

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

Combined_DF = pd.DataFrame()
bf_Dict_file = locate_A_File(["_BF_dictionaries.csv"],path)
Bf_Dict_File = pd.read_csv(bf_Dict_file)
PDG_file = locate_A_File(["cell_PDGs_zone_BF_values.csv"],path)
PDG_File = pd.read_csv(PDG_file).dropna()
bible_file = locate_A_File(["_bible_file.csv"],path)
Bible_File = pd.read_csv(bible_file,usecols = [0,1,4]).dropna()
Bible_File.columns = ['Sample_number' ,'Primordium','Day_or_night']

for sample_number in sample_list:

    growth_path = os.path.join(path, sample_number, "OUTPUT","GROWTH")
    PDG_path = os.path.join(path, sample_number, "OUTPUT","PDGs_ANISOTROPY")
    proli_path = os.path.join(path, sample_number, "OUTPUT","PROLIFERATION")
    meristem_file_path = os.path.join(path, sample_number, "OUTPUT","MERISTEM_ZONES")
    cell_dist_file_path = os.path.join(path, sample_number, "OUTPUT","DISTANCE_STUDY")
    cell_size_file_path = os.path.join(path, sample_number, "OUTPUT","CELL_SIZE")
    cell_curv_file_path = os.path.join(path, sample_number, "OUTPUT","CURVATURE")
    combined_file_path = os.path.join(path, sample_number, "OUTPUT","ZONE_PRIMORDIA","COMBINED_ZONES")

    for i in range(0,6):

        timepoint = "T"+str(i)

        prim_zone_file= locate_A_File([timepoint+"_combined_ZONES.csv"],combined_file_path)
        meristem_file= locate_A_File([timepoint+"_all_Meristem_zones.csv"],meristem_file_path)
        cell_dist_file= locate_A_File([sample_number +"_"+timepoint+"_cell_distance.csv"],cell_dist_file_path)
        cell_size_file= locate_A_File([sample_number +"_"+timepoint+"_CELL_SIZE.csv"],cell_size_file_path)
        cell_curv_file= locate_A_File([sample_number +"_"+timepoint+"_curvature.csv"],cell_curv_file_path)
        growth_file= locate_A_File ([sample_number +"_"+ timepoint,"_GROWTH.csv"],growth_path)#my data
        pdg_file= locate_A_File ([sample_number +"_"+ timepoint,"_PDGs.csv"],PDG_path)#my data
        proli_file= locate_A_File ([sample_number +"_"+ timepoint,"_PROLI.csv"],proli_path)#my data

        print (prim_zone_file)
        print (meristem_file)
        print (cell_dist_file)
        print (cell_size_file)
        print (cell_curv_file)

        #####################
        if ('' not in [prim_zone_file, meristem_file, cell_dist_file,cell_size_file, cell_curv_file]):

            Prim_Zone_File = pd.read_csv(prim_zone_file).dropna()
            Prim_Zone_File['Sample_number']= int(sample_number)
            Prim_Zone_File['Timepoint']= "T"+str(i)
            Prim_Zone_File = Prim_Zone_File[Prim_Zone_File['Zone'] != "1000"]
          
            Meristem_File = pd.read_csv(meristem_file).dropna()
            Meristem_File.columns = ['Label' ,'Zone']
            Meristem_File = Meristem_File[Meristem_File['Zone'] != 0]
            Meristem_File.loc[(Meristem_File['Zone'] == int(Zone_Dict["center"])),'Zone'] = "CZ"
            Meristem_File.loc[(Meristem_File['Zone'] == int(Zone_Dict["CZ"])),'Zone'] = "CZ"
            Meristem_File.loc[(Meristem_File['Zone'] == int(Zone_Dict["PZ"])),'Zone'] = "PZ"
            Meristem_File['Sample_number']= int(sample_number)
            Meristem_File['Timepoint']= "T"+str(i)

            Meristem_File = pd.merge(Meristem_File,Bf_Dict_File, on=['Sample_number','Timepoint'])            
            Meristem_File = pd.merge(Meristem_File,Bible_File, on=['Sample_number','Primordium'])            
            Prim_Zone_File = pd.merge(Prim_Zone_File,Bf_Dict_File, on=['Sample_number','Timepoint', 'Primordium'])
            Prim_Zone_File = pd.merge(Prim_Zone_File,Bible_File, on=['Sample_number','Primordium'])

            Meristem_File = Meristem_File[['Label','Zone','Primordium','Sample_number','Timepoint','BF_value','Day_or_night']]            
            Prim_Zone_File = Prim_Zone_File[['Label','Zone','Primordium','Sample_number','Timepoint','BF_value','Day_or_night']]

            All_Zones = pd.concat([Prim_Zone_File, Meristem_File], sort=False)

            ###  Adding cell distance, size and curvature information:
            Cell_Size_File = pd.read_csv(cell_size_file, usecols=[0,1]).dropna()
            Cell_Size_File.columns = ['Label' ,'Cell_size']
            Cell_Size_File['Label'] = pd.to_numeric(Cell_Size_File['Label'])
            Cell_Size_File['Sample_number']= int(sample_number)
            Cell_Size_File['Timepoint']= "T"+str(i)

            Obs_Files = pd.merge(All_Zones, Cell_Size_File, sort=False,how = "right")

            Cell_Dist_File = pd.read_csv(cell_dist_file).dropna()
            Cell_Dist_File.columns = ['Label' ,'Cell_distance']
            Cell_Dist_File['Sample_number']= int(sample_number)
            Cell_Dist_File['Timepoint']= "T"+str(i)

            Obs_Files = pd.merge(Obs_Files, Cell_Dist_File, sort=False,how = "left")

            Cell_Curv_File = pd.read_csv(cell_curv_file, usecols=[0,1]).dropna()
            Cell_Curv_File.columns = ['Label' ,'Cell_curvature']
            Cell_Curv_File['Label'] = pd.to_numeric(Cell_Curv_File['Label'])
            Cell_Curv_File['Sample_number']= int(sample_number)
            Cell_Curv_File['Timepoint']= "T"+str(i)

            Obs_Files = pd.merge(Obs_Files, Cell_Curv_File, sort=False,how = "left")

            ###  Adding cell growth, PDGs and proliferation information:
            print (growth_file)
            print (pdg_file)
            print (proli_file)

            if(proli_file and growth_file and pdg_file):
    
                Growth_File = pd.read_csv(growth_file, usecols = ['Label','Value']).dropna()
                Growth_File.columns = ['Label' ,'Growth']
                Growth_File['Timepoint']= "T"+str(i)
                Growth_File['Sample_number']= int(sample_number)
                Growth_File['Label'] = pd.to_numeric(Growth_File['Label'])
                Growth_File['Growth'] = Growth_File['Growth'].apply(lambda x: (x - 1)*100)

                Obs_Files = pd.merge(Obs_Files, Growth_File, sort=False,how = "left").drop_duplicates()
    
                PDG_File = pd.read_csv(pdg_file).dropna()
                PDG_File['Sample_number']= int(sample_number)
                PDG_File['Timepoint']= "T"+str(i)
                PDG_File['Label'] = pd.to_numeric(PDG_File['Label'])

                Obs_Files = pd.merge(Obs_Files, PDG_File, sort=False,how = "left").drop_duplicates()

                Proli_File = pd.read_csv(proli_file).dropna()
                Proli_File.columns = ['Label' ,'Proliferation']
                Proli_File['Sample_number']= int(sample_number)
                Proli_File['Timepoint']= "T"+str(i)
                Proli_File['Label'] = pd.to_numeric(Proli_File['Label'])

                Obs_Files = pd.merge(Obs_Files, Proli_File, sort=False,how = "left").drop_duplicates()
                # Obs_Files = Obs_Files[Obs_Files['Min'].isnull()]
                # print ('Obs_Files')
                # print (Obs_Files.describe())
                # print (Obs_Files.head(20))
                # print (len(list(Obs_Files['Label'])))
                # print (len(list(Obs_Files['Label'].unique())))
                # exit()
    
            Combined_DF = pd.concat([Combined_DF, Obs_Files], axis=0, ignore_index=True, sort=False)

# Combined_DF = Combined_DF.sort_values('Timepoint')
if(day_or_night in ["day_formed_primordia", "night_formed_primordia"]):
    Combined_DF = Combined_DF[Combined_DF.Day_or_night == filter_dict[day_or_night]]

print (Combined_DF.head(20))
print (Combined_DF.tail(20))

Combined_DF.to_csv(os.path.join(output,outfilename), index=False)