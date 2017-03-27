#!/usr/bin/env python

import sys
import time
import string
import calendar
from decimal import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import pylab
import matplotlib.dates as mdates
import calendar
import datetime
from datetime import datetime
from pytz import timezone
import pytz
import re
import os 
from dateutil import tz
from collections import Counter

# finpath1 = "/Users/BeiyuLin/Desktop/CPD/testCP.txt"    ## output CP data and needed to exclude the first 29 lines. 
# finpath2 = "/Users/BeiyuLin/Desktop/PopulationDensity/Test/test"  ## raw input data
# foutpath = "/Users/BeiyuLin/Desktop/PopulationDensity/Test/"
# write_duration_out_path = "/Users/BeiyuLin/Desktop/PopulationDensity/Test/Duration/"

finpath1 = "/Users/BeiyuLin/Desktop/CPD/atmoCP/CP_atmo1_data.al"    ## output CP data and needed to exclude the first 29 lines. 
finpath2 = "/Volumes/Seagate Backup Plus Drive/atmo/activityLables/atmo1_data.al"  ## raw input data
foutpath = "/Users/BeiyuLin/Desktop/PopulationDensity/"
write_duration_out_path = "/Users/BeiyuLin/Desktop/PopulationDensity/Duration/"

fin1 = open(finpath1, 'rU')   ## except the first 29 lines
f1 = fin1.readlines()
fin1.close()

fin2 = open(finpath2, 'rU')
f2 = fin2.readlines()
fin2.close()

len1 = len(f1)
len2 = len(f1)-29
len2_test = len(f2)

def activity_count(index0, index1):

	### filter out different activities. 
	activity_list = []
	sorted_counted_act = []
	for i in range(index0, index1+1):
		line_split = re.split("\t", activity_match_CP[i])
		# print("line_split",line_split)
		# ['1', '2015-07-29 22:03:34.845715', 'Other_Activity']
		activity_list.append(line_split[2].strip())

	#print("activity_list", activity_list)
	### check if all activities are Other_Activity
	if (all(x== "Other_Activity" for x in activity_list)):
		return (index1, "Other_Activity")
	else:
		len_a_l = len(activity_list)
		sorted_counted_act = Counter(activity_list).most_common(len_a_l)
		#### [("a", 2), ("b", 1)]
		#print("sorted_counted_act", sorted_counted_act)
		### consider the speical case that there are more than one majority in the sorted_counted_act list.
		if (sorted_counted_act[0][0] == "Other_Activity"):
			majority_index = 1
		else:		
			majority_index = 0 

		value_of_majoirty = sorted_counted_act[majority_index][1]  ## retun the value of the majority label. 
		
		#### the if is for the case: [("Other_Activity", 2), ("Wokr", 2)], then majoirty_index + 1 = 2 = len, it can not do for loop.
		if ((len(sorted_counted_act) == 1) or (len(sorted_counted_act) == 2 and (majority_index + 1 == 2 ))):
			return (index1, sorted_counted_act[majority_index][0])

		else:
			for i in range(majority_index + 1, len(sorted_counted_act)):
				if sorted_counted_act[i][1] == value_of_majoirty:   ## more than one majority label. 
					index1 += 1
					activity_count(index0, index1)   ## repeate until there is one majority. 
				return (index1, sorted_counted_act[majority_index][0])


##########################################################################################
########### match the 1 values and the 0 values with the time and the activity ###########
########### and write out to Mached_Activity_CP.txt using f1out ##########################
##########################################################################################
activity_match_CP = []
#f1out = open(foutpath + "Mached_Activity_CP.txt", 'w')
for i in range(28, len1):

	l1 = re.split(' ', f1[i])
	l2 = re.split(' ', f2[i])
	# print "l1", l1
	# print "l2", l2
	# l1 ['0', '503.817961111', '0\n']
	# l2 ['2015-07-31', '01:16:41.463489', 'EntrywayB', 'OFF', 'Enter_Home\n']
	#f1out.write(l1[2].strip() + "\t" + l2[0] + " " + l2[1] + "\t" + l2[4].strip() + '\n')
	activity_match_CP.append(l1[2].strip() + "\t" + l2[0] + " " + l2[1] + "\t" + l2[4].strip())
#f1out.close()
# activity_match_CP format
# 1	2015-07-29 22:03:34.845715	Other_Activity
# 0	2015-07-29 22:04:08.21665	Other_Activity

len_act_match = len(activity_match_CP)

index_start = 0
index_end = 0

##########################################################################################
########### find the majority lable in each segment and replace the activity label #######
########### write the labeled segment with timestamp into a file with f2out ##############
##########################################################################################
#f2out = open(foutpath + "Time_Activity.txt", 'w')
i = 0 
CP_activity = ""
returned_new_end_index = 0

activity_label_dict = {}

while( i < len_act_match -1 ):
	l_cur = re.split("\t", activity_match_CP[i])
	l_next = re.split("\t", activity_match_CP[i + 1])

	if int(l_cur[0]) == 1:
		index_start = i 
		i += 1
		continue

	elif (int(l_cur[0]) == 0 and int(l_next[0]) != 1):
		i += 1
		continue

	elif (int(l_cur[0]) == 0 and int(l_next[0]) == 1):
		index_end = i
		returned_new_end_index, CP_activity = activity_count(index_start, index_end)

		l_start = re.split("\t", activity_match_CP[index_start])
		l_end = re.split("\t", activity_match_CP[returned_new_end_index])

		##### write into a file ######
		#f2out.write(l_start[1] + '\t' + CP_activity + '\n')
		#f2out.write(l_end[1] + '\t' + CP_activity + '\n')

		format_time_start = time.mktime(datetime.strptime(l_start[1], "%Y-%m-%d %H:%M:%S.%f").timetuple())  ## 2015-07-29 22:07:30.926464
		format_time_end = time.mktime(datetime.strptime(l_end[1], "%Y-%m-%d %H:%M:%S.%f").timetuple())

		#### duration calculation ####
		duration = format_time_end - format_time_start
	
		if (CP_activity not in activity_label_dict.keys()):
			#print("CP_activity NOT IN KEY", CP_activity, activity_label_dict)
			activity_label_dict[CP_activity] = [duration]
		else:
			#print("CP_activity IN KEY", CP_activity, activity_label_dict)
			activity_label_dict[CP_activity].append(duration)

		index_start = returned_new_end_index + 1
		i = returned_new_end_index + 1
#f2out.close()

##########################################################################################
########### write the duration of each labeled activity into file ########################
##########################################################################################

#### test the coding is correct or not: make sure the len are the same ####
len_sum_l = 0
len_sum_t = 0

for key in activity_label_dict.keys():
	dur_out = open(write_duration_out_path + key + ".txt", 'w')
	for i in range(0, len(activity_label_dict[key])):
		dur_out.write(str(activity_label_dict[key][i]) + "\n")
		len_sum_t += 1
	len_sum_l = len_sum_l + len(activity_label_dict[key])
	dur_out.close()
print("The duration calculation is:", len_sum_l == len_sum_t)


















