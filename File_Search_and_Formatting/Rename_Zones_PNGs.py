#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

"""
Script to rename all files with a common regex.

INPUT:
======

File complete path location.

OUTPUT:
=======

Corresponding files with altered names, at the same location.

"""

file_path = "/home/user/Desktop/Project_2/210809_LEAF_DATA_EE/08/OUTPUT/ZONE_PRIMORDIA" # location of the files that needs formatting.
# ========================================

for file in os.listdir(file_path):
    if(file.endswith("_zone.png")):
        target_str = file[0:8]
        filename_pieces = target_str.split("_")
        new_filename = filename_pieces[0]+"_"+filename_pieces[2]+"_"+filename_pieces[1]
        new_file = file.replace(target_str,new_filename)
        os.rename(os.path.join(file_path,file), os.path.join(file_path, new_file))

