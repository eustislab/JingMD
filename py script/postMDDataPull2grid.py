import os as os
import numpy as numpy
import matplotlib.pyplot as plt
import sys
decimalPointForE = 3
decimalPointForf = 6


input=str(sys.argv[1])
numberOfExcitedStates=int(sys.argv[2])
path = os.getcwd()
inputPath=path+'/'+input

outputList=[]
fileList=os.listdir(inputPath)
listAllEAndf=[]
energies=[]
oscillatorStrengths=[]
timeList=[]
energyFinal=numpy.array(['Energy(eV)'])
oscillatorStrengthFinal=numpy.array(['Oscillator Strength'])
def mode(list):
    d = {}
    for elm in list:
        try:
            d[elm] += 1
        except(KeyError):
            d[elm] = 1    
    keys = d.keys()
    max = d[keys[0]]
    for key in keys[1:]:
        if d[key] > max:
            max = d[key]
    max_k = []      
    for key in keys:
        if d[key] == max:
            max_k.append(key),
    return max_k,max
for fileName in fileList:
    if ".log" in fileName:
        outputList.append(fileName)

f1=open(input+'MD_data.csv','w')
f2=open(input+'MD_dipole.csv','w')
for fileName in outputList:
	eachFile=inputPath+'/'+fileName
	f=open(eachFile,'r')
	lines=f.readlines()
	startingLine=0
	fileIsComplete=False
	for i, line in reversed(list(enumerate(lines))):
		if ' STATE #   1  ENERGY =    ' in line:
			startingLine=i
			fileIsComplete=True
			break
	if fileIsComplete:
		print 'Harvesting data from file named: '+fileName
		counter=0
		for n, line in enumerate(lines):
			#time
			if line.startswith('     RUN TITLE'):
				nextLine=lines[n+2]
				time=str(nextLine.split()[3])
				f1.write(time)
				f2.write(time)
			if line.startswith(' STATE # '):
				E=line.split()[5]
				nextLine=lines[n+1]
				f=nextLine.split()[3]
				f1.write(','+E+','+f)
				counter+=1
			if (counter==numberOfExcitedStates):
				f1.write('\n')
				counter=0
			if line.startswith('                          SUMMARY OF TDDFT RESULTS'):
				for linesAhead in range(5,5+numberOfExcitedStates):
					lineContainingDipoles=lines[n+linesAhead]
					lineSplit=lineContainingDipoles.split()
					[X,Y,Z]=[lineSplit[4], lineSplit[5], lineSplit[6]]
					f2.write(','+X+','+Y+','+Z)
				f2.write('\n')
    			
    			
    			