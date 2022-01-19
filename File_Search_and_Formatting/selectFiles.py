#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
import os
from datetime import datetime

"""

19/04/11: 

locateParents:
==============

	Function to locate Parenting data using given parameters.
	Input: locateParents(WT,09,T0,T4)
	Output: file_list =[.\WT_09\WT_09_PARENTS_T0T1.csv,.\WT_09\WT_09_PARENTS_T1T2.csv,.\WT_09\WT_09_PARENTS_T2T3.csv,.\WT_09\WT_09_PARENTS_T3T4.csv]


DataFrameToCsv:
===============

	Function that convert a dataframe of cell lineage ('Start' and 'End' labels) to a MGX compatible .csv file.
	Input : DataFrameToCsv(current_lineage_start_end,filename.csv)


"""

def locateParents(sample_number,timepoint_start,timepoint_end, path_of_search):

	# print "\nExecuting locateParents\n"
	# print "parameters are: ", sample_number,timepoint_start,timepoint_end, path_of_search
	interval_start = int(timepoint_start[1:])
	interval_end = int(timepoint_end[1:])
	Timepoints = []
	File_List = []
	
	for i in range(interval_start,interval_end+1):
		Timepoints.append("T"+str(i))
	# print ("\nTimepoints are: "), Timepoints
	# exit()
	for i,j in zip(Timepoints,Timepoints[1:]):
		
		my_file = sample_number + "_PARENTS_" + i + j + ".csv"
		for filename in os.listdir(path_of_search):
			if filename.endswith(my_file) :
				my_file = os.path.join(path_of_search, filename)
				File_List.append(my_file)

	return File_List

def locateParentsLayers(sample_layer,sample_number,timepoint_start,timepoint_end, path_of_search):
	
	interval_start = int(timepoint_start[1:])
	interval_end = int(timepoint_end[1:])
	Timepoints = []
	File_List = []
	# print sample_layer,sample_number,timepoint_start,timepoint_end, path_of_search, interval_start, interval_end
    
	for i in range(interval_start,interval_end+1):
		Timepoints.append("T"+str(i))

	for i,j in zip(Timepoints,Timepoints[1:]):
		
		my_file = sample_number +"_"+ sample_layer  + "_PARENTS_" + i + j + ".csv"
		for filename in os.listdir(path_of_search):
			if filename.endswith(my_file) :
				my_file = os.path.join(path_of_search, filename)
				File_List.append(my_file)
        # print my_file

	return File_List
	
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


def locate_in_Subs(File_Parameters,path):

    my_file=""
    # print "\nExecuting locate_in_Subs\n"
    # print "parameters are", File_Parameters
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if all(parameter in name for parameter in File_Parameters):
                my_file = os.path.join(root, name)
                # print "Found:",my_file
                # print "\nEnd locate_in_Subs\n"
    return my_file

def locate_Files_in_Subs(File_Parameters,path):

    File_List=[]
    # print "\nExecuting locate_Files_in_Subs\n"
    # print "parameters are", File_Parameters
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if all(parameter in name for parameter in File_Parameters):
                my_file = os.path.join(root, name)
                # print "Found:",my_file
                File_List.append(my_file)
    # print "\nEnd locate_Files_in_Subs\n"
    return File_List


def locateFiles(File_Parameters,path):
	
	my_file=""
	File_List = []
	
	# print "\nExecuting locateFiles\n"
	# print "parameters are", File_Parameters
	for filename in os.listdir(path):
		if all(parameter in filename for parameter in File_Parameters):
			my_file = os.path.join(path, filename)
			# print "Found:",my_file
			File_List.append(my_file)
	# print "\nEnd locateFiles\n"
	
	return File_List
	
def DataFrameToCsv(Dataframe,filename,path):

	timestamp = str(datetime.now().date()).replace("-","")[2:]
	file_path = os.path.join(path,timestamp+"_"+filename)
	output=open(file_path , 'w' )
	writer=csv.writer(output)
	headline=('Label',' Parent label')
	writer.writerow(headline)
	for index, row in Dataframe.iterrows():
		row=(int(row['Label']),int(row[' Parent Label']))
		
		# if the row is empty:
		if row != (0,0):
			writer.writerow(row)
	output.close()
	
	# print "\nLineage information file " , filename, " created.\n"
	
	return output
		
	
	
if __name__ == '__main__':

	File_Parameters =[]
	path = sys.argv[-1]
	
	for i in range(1,len(sys.argv)-1):
		
		File_Parameters.append(sys.argv[i])
		# print i, sys.argv[i]
		
	locate_A_File(File_Parameters,path)