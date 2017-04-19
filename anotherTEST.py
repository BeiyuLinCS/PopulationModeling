#!/usr/bin/env python
import sys
import time
import string
import calendar
from decimal import *
import numpy
import numpy as np
import csv
import calendar
import datetime
from datetime import datetime
from pytz import timezone
import pytz
import re
import os 
import ocpd as oncd
from functools import partial
import matplotlib.pyplot as plt
import pylab
import itertools



if __name__ == '__main__':
    #filename1, filename2 = sys.argv[1:3]
    finpath = "/Users/BeiyuLin/Desktop/bosch1EF.txt"
    #finpath0 = "/net/files/home/blin/PopulationModelling/ExtractedFeatures/EFGapTimeLabel"
    #finpath = finpath0 + filename1
    #print("read in file", filename1)

    data_in = np.array([], dtype = np.float64)
    count = 0

    f = open(finpath, 'rU')
    f_lines = f.readlines()
    count = len(f_lines)
    f.close()

    data = [[0]]*(count)

    for i in range(0, count):
        l_split = re.split('\t', f_lines[i])
        l_split[-1] = l_split[-1].strip()
        tdata = []
        for j in range(0, len(l_split)-1):
            tdata.append(np.round(float(l_split[j]),3))
        data[i] = tdata
        
    a = np.transpose(data)
    a = list(itertools.chain.from_iterable(a))
    a = np.round(a, decimals=3)
    
    R, maxes = oncd.online_changepoint_detection(count, a, oncd.StudentT(1, 1, 1, 0))
    final_score = maxes
    
    alarm=np.zeros(len(final_score))
    for i in range(1, len(final_score)):
        if (final_score[i]< final_score[i-1]):
            alarm[i-1]=1
    
    foutpath = "/Users/BeiyuLin/Desktop/CPbosch1EF.txt"
    
    fout = open(foutpath, 'w')
    for i in range(0, len(alarm)):
    	fout.write(str(alarm[i]) + "\n")
    fout.close()













