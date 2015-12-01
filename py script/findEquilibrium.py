import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import sys
import string
import numpy as np
#if this is called from plotEnergyMD then there is no need to ask for output name and redefine the variables again

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
#pull out CSV
f = csv.reader(open(output))
#convert column to array using zip (a built in function)
Time, Energy, Temp = zip(*f)
#convert string to float
Time = map(float, Time) 
Energy = map(float, Energy) 
Temp = map(float, Temp) 

#find Equilibrium - linear regression
minNumberOfStep=1000
#this is from aniline32.log - 15000 to 25000
maxSlope=1e-4
#for plotting
slope=[]
print 'Finding equilibrium using minimum number of steps = '+str(minNumberOfStep) +' and maximum slope = '+str(maxSlope)
try:
    size=len(Time)
    x=Time[0:minNumberOfStep]
    y=Energy[0:minNumberOfStep]
    #for using in loop
    lowestSlopeValue=1e5
    indexOfLowestSlope=-1
    for i in range(0,size-1-minNumberOfStep):
        print 'Finding equilibrium from t= '+str(Time[i])+' to '+str(Time[i+minNumberOfStep-1])
        m,b = np.polyfit(x, y, 1)
        slope.append(m)
        print 'slope = ' +str(m)
        if abs(m)<=abs(lowestSlopeValue):
            lowestSlopeValue=float(m)
            indexOfLowestSlope=int(i)
        #else remove the head and add next tail
        del x[0]
        x.append(Time[minNumberOfStep+i])
        del y[0]
        y.append(Energy[minNumberOfStep+i])
except IndexError:
        print 'There is not enough data to determine the equilibrium'
if abs(lowestSlopeValue)<=abs(maxSlope):
        print 'Found best equilibrium starting from '+str(Time[indexOfLowestSlope])+' to '+str(Time[indexOfLowestSlope+minNumberOfStep-1])+' with slope = '+str(lowestSlopeValue)

x=slope
y=Time[0:size-1-minNumberOfStep]
plt.plot(y,x)
plt.xlabel('Starting Time (fs)')
plt.ylabel('Slope (KCal/mol/fs)')
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2), useOffset=False)
plt.title('Slope vs Time for the MD File: ' + str(input))
plt.savefig(str(input) + '_SlopePlot.pdf', format='pdf')