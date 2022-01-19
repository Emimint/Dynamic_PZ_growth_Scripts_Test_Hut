#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import pandas as pd

"""

2021/06/06:

Script to automatically create a dictionnary between the developmental stage of primordium (here, we use the primordium BF (Boundary Formation) time - see main text) and the absolute time of the experiment for each sample.

INPUT:
======

bible file: manually created .csv file that inidicate, either for flower or leaf samples, for each primordium, its exact BF value and asbolute time of formation. It also indicates if the sample is formed during the day or the night.

timestamp_file: manually created .csv file that shows the following information for all project samples: sample type (leaf or flower), exact time and date of confocal scanning and wether or not it was included in the present paper.

OUTPUT:
=======

One "xx_Timepoint_BF_value_dictionnary.csv" file for each sample identified in the bible file.

"""

#"bible" file path (for flower or leaf samples):
my_file = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE/210921_all_flower_samples_bible_file.csv"
# timestamp_file path:
timestamp_file = "/home/user/Desktop/Project_2/210811_all_leaf_and_flower_data_timestamp_info_EE.csv"
# Dictionary destination folder:
# destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE" # path to  FLOWER DATA
destination_path = "/home/user/Desktop/Project_2/210623_FLOWER_DATA_EE" # path to LEAF DATA
data_type = "flower" # leaf or flower
# ========================================


# Conversion of "bible" file to dataframe:
File = pd.read_csv(my_file).dropna()
File.columns = ["Sample","Primordium","Time_boundary_formation","Formation_time","Day_or_night","Zone_definition_time"]

# Conversion of timestamp_file to dataframe:
Timestamp_File = pd.read_csv(timestamp_file, usecols= [0,1,7]).dropna()
Timestamp_File["Type"] = Timestamp_File["Type"].apply(lambda x:x.split(' ')[-1])
Timestamp_File["Sample"] = Timestamp_File["Sample"].apply(lambda x:x.split('_')[-1])
Timestamp_File["Included_in_analysis"] = Timestamp_File["Included_in_analysis"].astype(int)

# list of all samples in folder:
all_samples = File['Sample'].unique()

for sample in all_samples:

    sample_str = str(sample)
    if (len(str(sample)) == 1):
        outfile = "0"+str(sample)+"_Timepoint_BF_value_dictionnary.csv"
        sample_str = "0"+str(sample)

    Sample_DF = File[File['Sample'] == sample]
    
    # selecting current sample's timepoints which are part in analysis:
    Sample_Timestamp_File = Timestamp_File[(Timestamp_File['Sample'] == sample_str) & (Timestamp_File['Type'] == data_type) & (Timestamp_File.Included_in_analysis == 1)]
    
    print (Sample_Timestamp_File)

    number_of_TPs = len(Sample_Timestamp_File)
    TP_list = range(0,number_of_TPs)
    
    outfile = str(sample)+"_Timepoint_BF_value_dictionnary.csv"

    # creation of empty dictionnary DF:
    BF_File = pd.DataFrame(columns = ["BF_value","Timepoint","Primordium"])

    #BF_value : timepoint of boundary formation for a given primordium as shown in "bible" file:
    for index, row in Sample_DF.iterrows():
        BF_value = int(row[2][-1:])
        primordium = row[1]

        for i in TP_list:
            val = i - BF_value
            new_row = {'BF_value':val, 'Timepoint':'T'+str(i), 'Primordium':primordium}
            BF_File = BF_File.append(new_row, ignore_index=True)

    BF_File.to_csv(os.path.join(destination_path, outfile), index=False)


