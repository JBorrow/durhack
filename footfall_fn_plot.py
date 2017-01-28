'''
Code that plots footfall function
'''

import numpy as np
import matplotlib.pyplot as plt
def Temp(t):
    '''
    Function that returns the temperature for a given (array of) times
    '''
    out = t**2 + t + 2
    return out
    
def Precip(t):
    '''
    Function that returns the precipitation for a given (array of) times
    '''
    out = t + 5
    return out
    

#Parameters
ALPHA = 1.      # Fit parameter for temperature K
BETA = 1.       # Fit parameter for precipitation p
dt = 1.         # timestep (in days)
Df = 1.         # Rate of change of footfall df/dt - currently set to 1

#Calculation of footfall
times = np.linspace(0.,15.,40)  #initialise array of times
f = (ALPHA*Temp(times)*dt + BETA*Precip(times)*dt)*Df

#Plotting code
fig = plt.figure()
axes = plt.axes()
axes.set_xlabel("time")
axes.set_ylabel("footfall")
#ax.text(0.8,1.02,'T = %.2f' %intT, transform=ax.transAxes)
axes.text(0.1,1.02,'ALPHA = %.2f' %ALPHA, transform=axes.transAxes)
axes.text(0.4,1.02,'BETA = %.2f' %BETA, transform=axes.transAxes)
plt.plot(times,f)
plt.show()


