# -*- coding: utf-8 -*-
from __future__ import division 


"""
Module to predict footfall in durham city centre

Authors: S. Kailasa, H. Wang, J. Borrow
Durhack 2017

Written for Python 2, sorry :( (I'm a physicist)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#----------------------------------------------+ Loading Data +--------------------------------------------------------------------------------------
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

weeks_in_year	 = 53
days_in_week = 7
#---------------------------------------------+ Formatting Data +--------------------------------------------------------------------------------------

## Function to format data and return day weights

def day_multiplier(street_year):
	"""
	Function to normalise footfall data for the effects of a particular day of the week
	
	Inputs:
	------
	street_year : accepted inputs are - ss15, eb15, nr15 ss16 eb16 nr16 cp16 mp16 [var]

	Outputs: 
	-------
	year without day effect : array of footfall for the given year, without the effect of days [array]

	"""
	daily_footfall =  street_year.flatten()


	normalised_footfall = []

	for week in range(weeks_in_year):
		for weekday in range(days_in_week):
			normalised_footfall.append(street_year[week,weekday]/max(street_year[week,:]))


	normalised_footfall = np.array(normalised_footfall)

	normalised_footfall = np.reshape(normalised_footfall,(weeks_in_year,days_in_week))

	average_week = np.mean(normalised_footfall,axis = 0)

	relative_day_weights = np.mean(normalised_footfall[:-1],axis = 0) # ignoring weird last data point ---> check!

	day_multipliers = 1/(relative_day_weights/min(relative_day_weights))

	weighted_days = []

	for week in range(weeks_in_year):
		weighted_days.append(street_year[week,:]*day_multipliers)

	weighted_days = (np.array(weighted_days)).flatten()

	fig = plt.figure()

	plt.plot(weighted_days)
	plt.plot(daily_footfall)

	plt.show()


day_multiplier(nr16)


def month_multplier(street_year):
	"""
	function to remove the variation in footfall due to being in a particular month.
	Inputs:
	------
	street_year : accepted inputs are - ss15, eb15, nr15 ss16 eb16 nr16 cp16 mp16 [var]

	Outputs: 
	-------
	year without moth effect : array of footfall for the given year, without the effect of months [array]

	"""
