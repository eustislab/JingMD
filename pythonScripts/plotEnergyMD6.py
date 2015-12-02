###########################################################
###This version is created to deal with large file      ###
###The solution will be to use for line in f1 and avoid ###
###using readlines()                                    ###
###########################################################

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import sys
import string

#call as plotEnergyMD3.py inputfile

try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: plotEnergyMD.py input.log   \n' 
		sys.exit()
	else:
		input=str(sys.argv[1])
except IndexError:
    print '\n!!!Input command Error. Call function as: plotEnergyMD.py input.log \n' 
    sys.exit()

output=str(input) + '_energies.csv'
###############################
#clear (input).energies.csv
f = open(output, 'w');
f.write('')
#constant
lineBwTimeAndEnergy=0;
lineBwTimeAndTemp=0;
lineCountFromTime=0;
collectionStarted=False
foundTime=False
foundPE=False
foundTemp=False
firstTime=True
grandString=''

###############################
#functions
def printTime (thisLine):
    lineComponents=thisLine.split();
    timeString=str(lineComponents[3]);
    print "Analyzing t = "+timeString+" fsec\n"
    
def shouldCollectTime(line):
    #only check if collection is in progress
    if ' *** AT T=' in line:
        return True;
    else:
        return False;

def shouldCollectPE(line,reference,currentLine):
    #check if line bw time and energy is known 
    if reference>0:
        if currentLine==reference:
            return True
        else:
            return False
    #if not then it needs to be found using string
    elif reference==0:
        if '     POT  ENERGY' in line:
            reference=int(currentLine)
            return True;
        else:
            return False;

def shouldCollectTemp(line,reference,currentLine):
    #check if line bw time and energy is known 
    if reference>0:
        if currentLine==reference:
            return True
        else:
            return False
    #if not then it needs to be found using string
    elif reference==0:
        if '     TEMPER' in line:
            reference=int(currentLine)
            return True;
        else:
            return False;

def shouldWrite():
    #only check if collection is in progress
    if foundTime:
        if foundPE:
            if foundTemp:
                return True;
            else:
                return False
        else:
            return False;
    else:
        return False;

###############################
f = open(output, 'w');
f.write('')
#open input
print 'finding patterns...'
f1=open(input)
for line in f1:
    #this keyword is usually before coordinate
    #find out if collection is needed            
    if not foundTime:
        if shouldCollectTime(line):
            printTime(line)
            #split line
            lineComponents=line.split();
            #append time (split) to string
            #split line using space - sample(*** AT T=         10.00 FSEC, THIS RUN'S STEP NO.=      10)
            #this will be split to ['***', 'AT', 'T=', '10.00'...] -time = element 4
            grandString=grandString+str(lineComponents[3]);
            foundTime=True;
    elif not foundPE:
        if shouldCollectPE(line,lineBwTimeAndEnergy,lineCountFromTime):
            #append time (split) to string
            #split line using space - sample(     POT  ENERGY      =     -1.804578585E+05 KCAL/MOL)
            #this will be split to [..., '=', '-1.804578585E+05'...] -time = element 4
            lineComponents=line.split();
            grandString=grandString+','+str(lineComponents[3])
            foundPE=True
    elif not foundTemp:
        if not firstTime:
            if shouldCollectTemp(line,lineBwTimeAndTemp,lineCountFromTime):
                #append time (split) to string
                #split line using space - sample(     TEMPERATURE      =         349.98666547 K)
                #this will be split to [..., '=', '-349.98666547'...] -time = element 3
                lineComponents=line.split();
                grandString=grandString+', '+str(lineComponents[2])+'\n';
                foundTemp=True
        if firstTime:
            grandString=grandString+',0\n';
            firstTime=False
            foundTemp=True
    if shouldWrite():
        with open(output, 'a') as f:
            f.write(grandString)
        lineCountFromTime=0;
        collectionStarted=False
        foundTime=False
        foundPE=False
        foundTemp=False
        grandString=''
    lineCountFromTime+=1;


#pull out CSV
f = csv.reader(open(output))
#convert column to array using zip (a built in function)
Time, Energy, Temp = zip(*f)
#convert string to float
Time = map(float, Time) 
Energy = map(float, Energy) 
Temp = map(float, Temp) 


#plot
x = Time
y1 = Energy
y2 = Temp

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(x, y1, 'g-')
ax2.plot(x, y2, 'b-')

ax1.set_xlabel('Time (fs)')
ax1.set_ylabel('Potential Energy (KCal/mol)', color='g')
ax1.ticklabel_format(axis='y', style='sci', scilimits=(-2,2), useOffset=False)
ax2.set_ylabel('System Temperature (K)', color='b')
plt.title(r'       Potential Energy vs Time for the MD File: ' + str(input))
plt.savefig(str(input) + '_EnergyPlot.pdf', format='pdf')

#find Equilibrium - linear regression
print 'Finding Equilibrium'
try:
    minNumberOfStep=1000
    #this is from aniline32.log - 15000 to 25000
    maxSlope=0.00022
    size=len(Time)
    x=Time[0:minNumberOfStep-1]
    y=Energy[0:minNumberOfStep-1]
    for i in range(0,size-1):
        print 'Analyzing at t= '+Time[i]
        m,b = np.polyfit(x, y, 1)
        if m<=0.00022:
            break
            print 'Found equilibrium starting from '+Time[i]+' to '+Time[i+minNumberOfStep]
        #else remove the head and add next tail
        else:
            del x[0]
            x.insert(-1,Energy(minNumberOfStep+i))
except IndexError:
        print 'There are not enough data to determine the equilibrium'