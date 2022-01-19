#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime
import os
import os.path
import pandas as pd
import selectFiles # on choisit, en fonction des timepoints et des parametres choisis, les fichiers necessaires.



def CombineLineage(sample_number,My_File_List,destination_path):

    timestamp = str(datetime.now().date()).replace("-","")[2:]
    New_Directory = timestamp+'_'+'LINEAGE_COMBINE_RESULTS'
    path_to_New_Directory = os.path.join(destination_path,New_Directory)
    file_start = sample_number + "_LineageCombine_"
    
    #we create a LineageCombine directory as a subfolder if it does not exist yet at the current date:
    if os.path.exists(path_to_New_Directory):
        print ("\nThe directory %s already exits in %s" % (New_Directory,destination_path))
    else:
        try:
            os.mkdir(path_to_New_Directory)
        except OSError:
            print ("\nCreation of the directory %s failed" % New_Directory)
            exit()
        else:
            print ("\nSuccessfully created the directory %s in %s.\n" % (New_Directory,destination_path))
    
    Merged_Lineage = pd.DataFrame() 

    for file_lineage in My_File_List:
        print ("file_lineage", file_lineage)
        Lineage = pd.read_csv(file_lineage, usecols=[0,1]).dropna()
        Lineage.columns = ['Label',' Parent Label']
        Lineage = Lineage.astype(int)

        # Swap column is used to relocate the initial Lineage at the first table column position
        Lineage['Swap'] = Lineage['Label']
        Lineage['Label'] = Lineage[' Parent Label']
        Lineage[' Parent Label'] = Lineage['Swap']
        Lineage = Lineage.drop(columns='Swap')
            
        # first and second timepoints of the Lineage we just loaded (ex: T0 T1)
        the_timepoints = re.findall(r'T\d+',file_lineage)
        timepoint_first = the_timepoints[-2]
        timepoint_second = the_timepoints[-1]
        
        Lineage.columns = ['Label_at_'+ timepoint_first ,'Label_at_'+ timepoint_second]
        print ("\nCurrent lineage:\n")
        print (Lineage.head(10))
            
        if Merged_Lineage.empty:

            #initialisation:
            Merged_Lineage = Lineage
            print (Merged_Lineage.dtypes)
            # timepoint used to stitch together consecutive Lineages (ex T1 in T0_T1 and T1_T2):
            timepoint_merge = timepoint_second
            
            #file info:
            starting_timepoint = timepoint_first
            filename = file_start + timepoint_first
            
        else:
            # if the files follows each other:
            if timepoint_merge == timepoint_first: 
            
                Merged_Lineage = Merged_Lineage.merge(Lineage, on=Lineage.columns[0])
                # (((OPTIONAL))) creation of an intermediate file containing all the current Lineage history for later verification:
                Merged_Lineage.to_csv(os.path.join(path_to_New_Directory,"complete_lineage_info_from_start_to_"+timepoint_second+".csv"), index=False)
                filename = file_start + starting_timepoint + timepoint_second
                
                # creation of a file containing only the first and current Lineage history:
                Current_Lineage_Start_End = pd.DataFrame()
                Current_Lineage_Start_End["Label"] = Merged_Lineage.iloc[:,-1]
                Current_Lineage_Start_End[" Parent Label"] = Merged_Lineage.iloc[:,0]
                print (Current_Lineage_Start_End)
                
                #we removed N/A values:
                Current_Lineage_Start_End = Current_Lineage_Start_End.fillna(0)
                
                #we make sure that all values are integers:
                Current_Lineage_Start_End["Label"] = Current_Lineage_Start_End["Label"].astype(int)
                Current_Lineage_Start_End[" Parent Label"] = Current_Lineage_Start_End[" Parent Label"].astype(int)
                
                print ("\nCurrent_Lineage_Start_End is:\n")
                print (Current_Lineage_Start_End.head(10))
                print  (Current_Lineage_Start_End.dtypes )
                #DataFrameToCsv will prevent float conversion of the data (floats won't be accepted in MGX) and remove empty rows:
                
                current_lineage_file = selectFiles.DataFrameToCsv(Current_Lineage_Start_End, filename + ".csv",path_to_New_Directory)
                # My_Final_File_List.append(current_lineage_file)
                
                #new stich point:
                timepoint_merge = timepoint_second
            else:
                
                # if the next file is not consecutive to the previous file then:
                Merged_Lineage = Lineage
                print (os.path.join(path_to_New_Directory,timepoint_first+"_to_"+timepoint_second+".csv"))
                Merged_Lineage.to_csv(os.path.join(path_to_New_Directory,timepoint_first+"_to_"+timepoint_second+".csv"), index=False)
                # timepoint and file information are updated:
                timepoint_merge = timepoint_second
                start = timepoint_first
                filename = file_start + timepoint_first
                starting_timepoint = timepoint_first
              
    return path_to_New_Directory

