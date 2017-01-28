# -*- coding: utf-8 -*-
from __future__ import division 
'''
Code to read/convert footfall excel data to numpy arrays
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize

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


climate = pd.read_excel('daily_basics.xls','daily')
climate.as_matrix()
climate_data_15_16 = np.array(climate)


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



## plots footfall each day on silver street


daily_footfall_ss_16 =  ss16.flatten()

fig = plt.figure()

ax = fig.add_subplot(111)

ax.plot(np.arange(0,len(daily_footfall_ss_16)),daily_footfall_ss_16)

saturdays_s16 = daily_footfall_ss_16[5::7]
saturdays_s16_day_no = np.arange(0,len(daily_footfall_ss_16))[5::7]

sunday_s16 = daily_footfall_ss_16[6::7]
sundays_s16_day_no = np.arange(0,len(daily_footfall_ss_16))[6::7]

ax.scatter(saturdays_s16_day_no,saturdays_s16,color = 'g',label = 'saturdays')
ax.scatter(sundays_s16_day_no,sunday_s16,color = 'r',label = 'sundays')

ax.set_xlabel('day')

ax.set_ylabel('footfall')
ax.legend()

plt.show()


## overlaying all of the weeks on silver street

'''fig = plt.figure()
ax = fig.add_subplot(211)

for week in range(53):
	ax.plot(ss16[week,:])

ax.set_title('silver street 2016 ')
ax.set_ylabel('footfall')

ax1 = fig.add_subplot(212)
for week in range(53):
	ax1.plot(ss15[week,:])

ax1.set_title('silver street 2015 ')
ax1.set_xlabel('week day')
ax1.set_ylabel('footfall')


plt.show()'''

'''
print climate_data_15_16.shape

fig = plt.figure()
ax = fig.add_subplot(211)

ax.plot(climate_data_15_16[:,1][:371])

ax1 = fig.add_subplot(212)
ax1.plot(daily_footfall_ss_16)

plt.show()
'''

normalised_ss16 = []

for week in range(53):
	for weekday in range(7): 
		 normalised_ss16.append(ss16[week,weekday]/max(ss16[week,:]))


normalised_ss16 = np.array(normalised_ss16)

normalised_ss16 = np.reshape(normalised_ss16,(53,7))
average_week_function = np.mean(normalised_ss16,axis = 0) 



reordered_chunks = [[] for x in xrange(len(average_week_function))] 

for waveform in range(len(normalised_ss16)):
    for chunk in range(len(average_week_function)):
        reordered_chunks[chunk].append(normalised_ss16[waveform][chunk])
    
mean_waveform = []
std_dev = []

for chunk in range(len(reordered_chunks)):
    std_dev.append(np.std(reordered_chunks[chunk]))


std_dev[-1] = 0

fig = plt.figure()

ax = fig.add_subplot(111)

ax.plot(average_week_function)

ax.fill_between(np.arange(0,7),average_week_function-std_dev, average_week_function+std_dev, color='grey', alpha='0.5')

plt.show()



relative_day_weights =  np.mean(normalised_ss16[:-1], axis = 0) # ignoring last datapoint - had something weird in it


day_multipliers = 1/( relative_day_weights/(min(relative_day_weights)))


ss16_weighted_days = []

for week in range(53):
	ss16_weighted_days.append(ss16[week,:]*day_multipliers)


ss16_weighted_days = (np.array(ss16_weighted_days)).flatten()

fig = plt.figure()

plt.plot(ss16_weighted_days)
plt.plot(daily_footfall_ss_16)

plt.show()


