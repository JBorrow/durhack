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
from scipy.optimize import leastsq
from scipy.optimize import curve_fit


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
days_in_month = 28
weeks_in_month = days_in_month/days_in_week
#---------------------------------------------+ Formatting Data +--------------------------------------------------------------------------------------

## Function to format data and return day weights



def term_model(	t, amplitude, wavenumber,phase ,baseline):
	"""artificial model for term times
	"""

	return amplitude* (np.sin(wavenumber*t + phase))**2 + baseline

def day_month_correction(street_year):
	"""
	Function to normalise footfall data for the effects of a particular day of the week and a particular month
	
	Inputs:
	------
	street_year : accepted inputs are - ss15, eb15, nr15 ss16 eb16 nr16 cp16 mp16 [var]

	Outputs: 
	-------
	weighted_days_and_months  : array of footfall for the given year, without the effect of days or months [array]

	"""
	daily_footfall =  street_year.flatten()


	# normalising for the effect of different days

	normalised_footfall = []

	for week in range(weeks_in_year):
		for weekday in range(days_in_week):
			normalised_footfall.append(street_year[week,weekday]/max(street_year[week,:]))


	normalised_footfall = np.array(normalised_footfall)

	normalised_footfall = np.reshape(normalised_footfall,(weeks_in_year,days_in_week))

	average_week = np.mean(normalised_footfall,axis = 0)

	relative_day_weights = np.mean(normalised_footfall[:-1], axis = 0) # ignoring weird last data point ---> check!

	day_multipliers = 1/(relative_day_weights/min(relative_day_weights))

	weighted_days = []

	for week in range(weeks_in_year):
		weighted_days.append(street_year[week,:]*day_multipliers)

	weighted_days = (np.array(weighted_days)).flatten()


	# normalising for the effect of different months
	months_in_year = int(len(daily_footfall)/days_in_month)

	extra_days =  int((len(daily_footfall)/days_in_month - months_in_year)*days_in_month) # dodgy fix for int number of months

	normalised_footfall = np.array(normalised_footfall)
	normalised_footfall = normalised_footfall.flatten()
	normalised_footfall = normalised_footfall[:-extra_days]


	normalised_footfall = np.reshape(normalised_footfall,(-1,1))

	normalised_footfall = np.reshape(normalised_footfall,(months_in_year,days_in_month))



	relative_month_weights = np.mean(normalised_footfall,axis = 1)


	month_multpliers = 1/(relative_month_weights/min(relative_month_weights))


	weighted_days = weighted_days[:-extra_days]


	weighted_days = np.reshape(weighted_days,(months_in_year,days_in_month))
	weighted_days_and_months = []
	for month in range(months_in_year):
		weighted_days_and_months.append(weighted_days[month]*month_multpliers[month])

	weighted_days_and_months = np.array(weighted_days_and_months).flatten()
	
	res = abs(weighted_days_and_months - weighted_days.flatten())


	return (weighted_days_and_months.astype(float),day_multipliers,month_multpliers)





def term_correction(street_year_day_month):

	data = day_month_correction(street_year_day_month)
	y = data[0]

	y = y.flatten()

	t = np.arange(0,len(y))

	guess_amplitude = 3*np.std(y)/(2**0.5)
	guess_wavenumber = 0.025
	guess_phase = 0.5
	guess_baseline = np.median(y)

	p0 = [guess_amplitude,guess_wavenumber,guess_phase,guess_baseline]

	fit = curve_fit(term_model, t, y, p0=p0)

	data_fit = term_model(t, *fit[0])

	data_first_guess = term_model(t, *p0)
	correction =fit[0][3]*2 

	corrected_term =  (y + (correction - data_fit))/2
	fig =plt.figure()
	axes = plt.axes()
	plt.plot(corrected_term, color='orange',label='corrected data')
	plt.plot(y,'.',color= 'blue', label='no corrections')
	plt.legend(loc='upper left')
	axes.set_xlabel("days")
	axes.set_ylabel("footfall")
	
	plt.show()

	return (corrected_term, fit[0], data[1], data[2]) # returning all fit parameters + fully corrected footfall


def footfall_model(street_year):
	"""
	takes predicted parameters from correction functions returns footfall
		
	"""
	data = term_correction(street_year)

	corrected_footfall = data[0].flatten()
	t = np.arange(0,len(corrected_footfall))

	params = [data[1],data[2],data[3]]

	day_multipliers = data[2]
	month_multpliers = data[3]


	baseline = np.mean(corrected_footfall[:-1])
	baseline = np.zeros(len(corrected_footfall)) + baseline

	
	# first plug in effects of terms - sine correction

	sine_correction = term_model(t,*params[0])

	baseline_and_sine = (sine_correction + baseline) 

	baseline_and_sine = np.reshape(baseline_and_sine,((13,days_in_month)))

	baseline_and_sine_and_month = []
	for month in range(len(baseline_and_sine)):
		baseline_and_sine_and_month.append(month_multpliers[month]*baseline_and_sine[month])


	day_multipliers_list = list(day_multipliers)*int(384/7)

	return day_multipliers_list

	 

print footfall_model(ss16)
