#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import csv
import sys
import os


dir_path = "/home/user/Desktop/ZONE_PRIMORDIA"



for filename in os.listdir(dir_path):

    print filename
    if filename.endswith("ZONES.csv"):
        df = pd.read_csv(os.path.join(dir_path,filename)).dropna()
        df.columns = ['Label','Zone']
        df['Zone'] = df['Zone'].replace(15, 1000)
        df.to_csv(os.path.join(dir_path,filename), index=False)
