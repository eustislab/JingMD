###########################################################
### This is used to determined the equilibrium using    ###
### linear regression and an upper limit for the slope	###
### The set range for this script is 10 ps          	###
###########################################################

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import sys
import numpy as np

#for asking what the input in terminal should be
try:
    if str(sys.argv[1])=='?':
        print '\nCall function as: findEquilibrium.py input.log   \n' 
        sys.exit()
    else:
        input=str(sys.argv[1])
except IndexError:
    print '\n!!!Input command Error. Call function as: findEquilibrium.py input.log \n' 
    sys.exit()
output=str(input) + '_energies.csv'
#This portion is the same as in plotEnergyMD6
#pull out CSV
f = csv.reader(open(output))
#convert column to array using zip (a built in function)
Time, Energy, Temp = zip(*f)
#convert string to float
Time = map(float, Time) 
Energy = map(float, Energy) 
Temp = map(float, Temp) 

#find Equilibrium using linear regression
#this number control the range of time to be used in energy fluctuation calculation
minNumberOfStep=1000
#This is the limit above which the script will report no equilibrium is found 
#this is from aniline32.log - 15000 to 25000
maxSlope=1e-4
#for plotting
slope=[]
print 'Finding equilibrium using minimum number of steps = '+str(minNumberOfStep) +' and top limit of acceptable slope = '+str(maxSlope)
try:
	#for looping
    size=len(Time)
    x=Time[0:minNumberOfStep]
    y=Energy[0:minNumberOfStep]
    #for using in loop
    #set thio a high value - it can be any number bc we will replace it with the lowest slope value found in loop
    lowestSlopeValue=1e5
    #Same - this will be replaced
    indexOfLowestSlope=-1
    for i in range(0,size-1-minNumberOfStep):
        print 'Finding equilibrium from t= '+str(Time[i])+' to '+str(Time[i+minNumberOfStep-1])
        #poly fit is basically a linear fit - m=slope, b=y_intersect
        m,b = np.polyfit(x, y, 1)
        #for plotting - append to array of existing slope values
        slope.append(m)
        print 'slope = ' +str(m)
        #take absolute value and see which interval does not fluctuate the least
        if abs(m)<=abs(lowestSlopeValue):
            lowestSlopeValue=float(m)
            indexOfLowestSlope=int(i)
        #this is similar to queue structure - room for improvement is to make x and y arrays into actual queues
        #else remove the head and add next tail
        del x[0]
        x.append(Time[minNumberOfStep+i])
        del y[0]
        y.append(Energy[minNumberOfStep+i])
#if x or y does not have enough element (minNumberOfStep) then report error
#room for improvement - move this up top instead of having a long try
except IndexError:
        print 'There is not enough data to determine the equilibrium'
#if lowestSlopeValue pass the top limit then report
if abs(lowestSlopeValue)<=abs(maxSlope):
	report=str('Found best equilibrium starting from '+str(Time[indexOfLowestSlope])+' to '+str(Time[indexOfLowestSlope+minNumberOfStep-1])+' with slope = '+str(lowestSlopeValue))
	print report
#if not then say so
else:
	report = 'Equilibrium is not yet reach'
	print report
	print str('The current limit is at '+str(maxSlope) +' kcal/mol/fs and the lowest value of slope = '+str(lowestSlopeValue))
	
#plot slope vs time
x=slope
#align time with slope
y=Time[0:size-1-minNumberOfStep]
plt.plot(y,x)
plt.gca().set_position((.125, .2, .8, .7))
plt.xlabel('Starting Time (fs)')
plt.ylabel('Slope (KCal/mol/fs)')
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2), useOffset=False)
plt.title('Slope vs Time for the MD File: ' + str(input))
plt.figtext(.01, .05,report)
plt.savefig(str(input) + '_SlopePlot.pdf', format='pdf')