# -*- coding: utf-8 -*-
from __future__ import division 
'''
Code to read/convert footfall excel data to numpy arrays
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

data15 = pd.read_excel('footfall_2015_16.xlsx', '2015')#, index_col=None, na_values=['NA'])
data15.as_matrix()
full_data15 = np.array(data15)          # Full 2015 data set as a numpy array
ss15 = full_data15[1:54,8:15]        # footfall for silver street from monday-sunday in 2015
eb15 = full_data15[1:54,17:24]       # -----------elvet bridge
nr15 = full_data15[1:54,25:32]       # -----------north road
events15 = full_data15[1:54,0:7]     # event data for 2015 (monday-sunday)

data16 = pd.read_excel('footfall_2015_16.xlsx', '2016')
data16.as_matrix()
full_data16 = np.array(data16)
ss16 = full_data16[1:54,8:15]
eb16 = full_data16[1:54,17:24]
nr16 = full_data16[1:54,26:33]
cp16 = full_data16[1:54,35:42]       # footfall data for claypath in 2016
mp16 = full_data16[1:54,44:51]       # footfall data for market place in 2016


day_labels = ['m','t','w','th','f','sa','su']

# plots the footfall for each day over all of the weeks in the year on silver street

fig = plt.figure()

ax = fig.add_subplot(211)

for day in range(len(day_labels)):
	ax.plot(ss16[:,day],label = day_labels[day])

ax1 = fig.add_subplot(212)
for day in range(len(day_labels)):
	ax1.plot(ss15[:,day], label = day_labels[day])

ax.legend()
ax1.legend()
ax1.set_xlabel('week number')

ax.set_ylabel('footfall')
ax1.set_ylabel('footfall')

# plt.show()

# plots the mean footfall weekend/weekday silver street

wknd_ss_16 = (ss16[:,-1]+ss16[:,-2]+ss16[:,-3])/3

wkday_ss_16 = np.sum(ss16[:,:5], axis = 1)/4


wknd_ss_15 = (ss16[:,-1]+ss15[:,-2]+ss15[:,-3])/3

wkday_ss_15 = np.sum(ss15[:,:5], axis = 1)/4


#fig = plt.figure()

ax = fig.add_subplot(111)

ax.plot(wknd_ss_16,label = 'weekend (+friday) 16')
ax.plot(wkday_ss_16, label = 'weekday (mon-th) 16')
ax.plot(wknd_ss_15,label = 'weekend (+friday) 15')
ax.plot(wkday_ss_15, label = 'weekday (mon-th) 15')
ax.set_ylabel('footfall')
ax.set_xlabel('week number')
ax.legend()
#plt.show()


## plots footfall each day on silver street




daily_footfall_ss_16 =  ss16.flatten()

fig = plt.figure()

ax = fig.add_subplot(111)

ax.scatter(np.arange(0,len(daily_footfall_ss_16)),daily_footfall_ss_16)

saturdays_s16 = daily_footfall_ss_16[5::7]
saturdays_s16_day_no = np.arange(0,len(daily_footfall_ss_16))[5::7]

ax.scatter(saturdays_s16_day_no,saturdays_s16,color = 'r')

plt.show()




