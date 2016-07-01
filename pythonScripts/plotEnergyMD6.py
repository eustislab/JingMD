###########################################################
### Use this to plot energy vs time to see if MD has    ###
### run its course. Generates: csv of PE and            ###
### temperature vs time, pdf of the plot                ###
###########################################################

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import sys
import string

#call as plotEnergyMD3.py inputfile
#for asking what the input in terminal should be
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

#initiate variables
lineBwTimeAndEnergy=0;
lineBwTimeAndTemp=0;
lineCountFromTime=0;
collectionStarted=False
foundTime=False
foundPE=False
foundTemp=False
firstTime=True
grandString=''
time='0'

###############################
#functions

#check if time is in line
def shouldCollectTime(line):
    #only check if collection is in progress
    if ' *** AT T=' in line:
        return True;
    else:
        return False;

# for printing time so one can keep track of the progress
def printTime (thisLine):
    lineComponents=thisLine.split();
    timeString=str(lineComponents[3]);
    print "Analyzing t = "+timeString+" fsec\n"

#Are we currently looking potential energy?
def shouldCollectPE(line,reference,currentLine):
    #check if line bw time and energy is known - this is written as reference
    if reference>0:
        if currentLine==reference:
            return True
        else:
            return False
    #if reference is not known, then it needs to be found by finding string POT EN...
    elif reference==0:
        if '     POT  ENERGY' in line:
            reference=int(currentLine)
            return True;
        else:
            return False;
#Are we currently looking Temp?
def shouldCollectTemp(line,reference,currentLine):
    #check if line bw time and energy is known - reference
    if reference>0:
        if currentLine==reference:
            return True
        else:
            return False
    #if not then it needs to be found by searching for the string TEMPER...
    elif reference==0:
        if '     TEMPER' in line:
            reference=int(currentLine)
            return True;
        else:
            return False;

#once everything is found, we should write down before moving on to the next snapshot
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
#open csv and prepare for writing
f = open(output, 'w');
f.write('')

#open input
f1=open(input)
print 'finding patterns...'
#avoid using readlines() so there'll be no problem with large files
for line in f1:
    #time keyword is before PE, PE is before Temp so the search should be in this order in order to be most efficient
    #find out if collection is needed            
    if not foundTime:
        if shouldCollectTime(line):
            printTime(line)
            #split line
            lineComponents=line.split();
            #append time (split) to string
            #split line using space - sample(*** AT T=         10.00 FSEC, THIS RUN'S STEP NO.=      10)
            #this will be split to ['***', 'AT', 'T=', '10.00'...] -time = element 4
            newTime=str(lineComponents[3])[:-3]
            if int(time)>=int(newTime):
            	print 'there is a duplication at '+time+' and '+newTime +' ignoring new values'
            else:
				time=str(newTime)
				grandString=grandString+time;
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
        #problem with this is - the first snapshot's temperature is not given in the log file
        #set Temp to 0 to indicate the beginning
        if firstTime:
            grandString=grandString+',0\n';
            #once append, turn off the boolean
            firstTime=False
            foundTemp=True
    #write after all data is collected for one snapshot
    if shouldWrite():
        with open(output, 'a') as f:
            f.write(grandString)
        #reset the variables
        lineCountFromTime=0;
        collectionStarted=False
        foundTime=False
        foundPE=False
        foundTemp=False
        grandString=''
    lineCountFromTime+=1;
#finish writing csv
f.close()

#plot
#pull out CSV
#use csv.reader bc csv has ',' and this automate the formatting
f = csv.reader(open(output))
#convert column to array using zip (a built in function)
Time, Energy, Temp = zip(*f)
#convert string to float
Time = map(float, Time) 
Energy = map(float, Energy) 
Temp = map(float, Temp) 

minEnergy=min(Energy)
relativeEnergy=[]
for eachEnergy in Energy:
	relativeEnergy.append(eachEnergy-minEnergy) 

#plot
x = Time
y1 = Energy
y2 = Temp

plt.subplot(2, 1, 1)
plt.plot(x, y1, 'g-')
plt.title('MD PE and T plot of: ' + str(input))
plt.ylabel('Potential Energy (KCal/mol)')

plt.subplot(2, 1, 2)
plt.plot(x, y2, 'b-')
plt.xlabel('time (fs)')
plt.ylabel('System Temperature (K)')
plt.savefig(str(input) + '_EnergyPlot.pdf', format='pdf')

plt.gcf().clear()
y1 = relativeEnergy

plt.subplot(2, 1, 1)
plt.plot(x, y1, 'g-')
plt.title('MD relative PE and T plot of: ' + str(input))
plt.ylabel('Relative Potential Energy (KCal/mol)')

plt.subplot(2, 1, 2)
plt.plot(x, y2, 'b-')
plt.xlabel('time (fs)')
plt.ylabel('System Temperature (K)')
plt.savefig(str(input) + '_EnergyPlot_2.pdf', format='pdf')