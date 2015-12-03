###########################################################
### Use this pull out excited state energies and dipole ###
### moments from all the files in specified folder      ###
### Output is time, S1, S2... or time, X1, Y1, Z1, X2...###
###########################################################

import os as os
import numpy as numpy
import matplotlib.pyplot as plt
import sys

#if not sure use ? to ask
try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: postMDDataPull2.py inputDirectory NumberOfExcitedStateEnergies\n' 
		sys.exit()
except IndexError:
    print '\n!!!Input command Error. Call function as: postMDDataPull2.py inputDirectory NumberOfExcitedStateEnergies\n' 
    sys.exit()

#Call as fincut.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules startTime stopTime timePerFrame
try:
    input=str(sys.argv[1])
	numberOfExcitedStates=int(sys.argv[2])
except IndexError:
    print '\n!!!Input command Error. Call function as: postMDDataPull2.py inputDirectory NumberOfExcitedStateEnergies\n' 
    sys.exit()
# to prevent / at the end of the input file if used terminal autofill
if input.endswith('/'):
    input = input[:-1]

#make input path - folder containing the log files or out files
path = os.getcwd()
inputPath=path+'/'+input

#arrays for storing and manipulating the data extracted
outputList=[]
fileList=os.listdir(inputPath)
listAllEAndf=[]
energies=[]
oscillatorStrengths=[]
timeList=[]
energyFinal=numpy.array(['Energy(eV)'])
oscillatorStrengthFinal=numpy.array(['Oscillator Strength'])
    
#get all the file names
for fileName in fileList:
    if (".out" in fileName or ".log" in fileName):
        outputList.append(fileName)

#open 2 output files
f1=open(input+'MD_data.csv','w')
f2=open(input+'MD_dipole.csv','w')
#now read each file and collect data
for fileName in outputList:
	eachFile=inputPath+'/'+fileName
	f=open(eachFile,'r')
	lines=f.readlines()
	startingLine=0
	fileIsComplete=False
	#find if the file is complete
	# use enumerate and reverse
	for i, line in reversed(list(enumerate(lines))):
		if ' STATE #   1  ENERGY =    ' in line:
			startingLine=i
			fileIsComplete=True
			break
	# now start collecting data
	if fileIsComplete:
		print 'Harvesting data from file named: '+fileName
		counter=0
		#loop
		for n, line in enumerate(lines):
			#time
			if line.startswith('     RUN TITLE'):
				nextLine=lines[n+2]
				time=str(nextLine.split()[3])
				f1.write(time)
				f2.write(time)
			#energy
			if line.startswith(' STATE # '):
				E=line.split()[5]
				nextLine=lines[n+1]
				f=nextLine.split()[3]
				f1.write(','+E+','+f)
				counter+=1
			#stop collecting
			if (counter==numberOfExcitedStates):
				f1.write('\n')
				counter=0
			#dipole
			if line.startswith('                          SUMMARY OF TDDFT RESULTS'):
				#5 lines are from 'SUMMARY...' to ' 1  A ...' which starts to contain dipole moments
				for linesAhead in range(5,5+numberOfExcitedStates):
					lineContainingDipoles=lines[n+linesAhead]
					lineSplit=lineContainingDipoles.split()
					#locations of dipole in line 
					[X,Y,Z]=[lineSplit[4], lineSplit[5], lineSplit[6]]
					f2.write(','+X+','+Y+','+Z)
				f2.write('\n')	