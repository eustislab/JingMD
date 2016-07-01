###########################################################
### Create inp for MD run from xyz file from packmol    ###
### ssbp radius is also calculated roughly from         ###
### starting geometry                                   ###
###########################################################

import sys
import csv
import os
import string


#for asking what the input in terminal should be
try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: prepareMD.py input.xyz numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules \n' 
		sys.exit()
except IndexError:
    print '\n!!!Input command Error. Call function as: prepareMD.py input.xyz numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules \n' 
    sys.exit()
#for assigning received input from terminal
try:
    input=str(sys.argv[1])
    numberofSoluteAtoms=int(sys.argv[2])
    numberofSoventAtoms=int(sys.argv[3])
    numberOfSolventMolecules=int(sys.argv[4])
except IndexError:
    print '\n!!!Input command Error. Call function as: prepareMD.py input.xyz numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules \n' 
    sys.exit()
#generate output name
if input.endswith('.xyz'):
    output = input[:-4]+'.inp'
#for safety - at worst the output will not overwrite the input
else:
    output=input+'.inp'

#part one
#This part is for finding ssbp radius for inout file
#enumerate gets data in line - line and line index - n
radiusInSolute=0.0
radiusInSolvent=0.0
avgX=0.0
avgY=0.0
avgZ=0.0
X=[]
Y=[]
Z=[]

lineNumber=0
#open input
f2=open(input)
for line in f2:
	lineNumber+=1
	#first two line does not contain useful info - x y z start on the third line
	if lineNumber>2:
		#x y z
		lineSplit=line.split()
		X.append(float(lineSplit[1]))
		Y.append(float(lineSplit[2]))
		Z.append(float(lineSplit[3]))
#for looping through array below
size=len(X)
#find a CG for solute atoms
avgX=sum(X[:numberofSoluteAtoms-1])/numberofSoluteAtoms
avgY=sum(Y[:numberofSoluteAtoms-1])/numberofSoluteAtoms
avgZ=sum(Z[:numberofSoluteAtoms-1])/numberofSoluteAtoms
#looping to find radius of each atoms in relative to solute's CG
#also find the maximum value of them
for i in range(0,size):
		d=((X[i]-avgX)**2+(Y[i]-avgY)**2+(Z[i]-avgZ)**2)**0.5
		if i<numberofSoluteAtoms:
			if radiusInSolute<d:
				radiusInSolute=d
		else:
			if radiusInSolvent<d:
				radiusInSolvent=d

#radius should be a little bit larger than the two combined - 3 Angstrom larger - this does not need to be super accurate
radiusInSolute=radiusInSolute
radiusInSolvent=radiusInSolvent
ssbpRadius=radiusInSolute+radiusInSolvent+3
print '\n'
print 'Radius in solute is:\t'+str(radiusInSolute)
print 'Radius in solvent is:\t'+str(radiusInSolvent)
print 'ssbp Radius should be:\t'+str(ssbpRadius)
print '\n'
###############################

#Part two - this is where geometry data is taken from xyz, change into GAMESS input's format + other input
numberOfAllSolventsAtoms=numberofSoventAtoms*numberOfSolventMolecules
fragmentNumber=1;
atomLabel=1

#this dict is for generating atomic number from Acronym
atomicNumber={'LV': 116.0, 'BE': 4.0, 'FR': 87.0, 'BA': 56.0, 'BH': 107.0, 'BI': 83.0, 'BK': 97.0, 'EU': 63.0, 'FE': 26.0, 'BR': 35.0, 'ES': 99.0, 'FL': 114.0, 'FM': 100.0, 'RG': 111.0, 'RU': 44.0, 'NO': 102.0, 'NA': 11.0, 'NB': 41.0, 'ND': 60.0, 'NE': 10.0, 'RE': 75.0, 'RF': 104.0, 'LU': 71.0, 'RA': 88.0, 'RB': 37.0, 'NP': 93.0, 'RN': 86.0, 'RH': 45.0, 'B': 5.0, 'CO': 27.0, 'TH': 90.0, 'CM': 96.0, 'CL': 17.0, 'H': 1.0, 'CA': 20.0, 'CF': 98.0, 'CE': 58.0, 'N': 7.0, 'CN': 112.0, 'P': 15.0, 'GE': 32.0, 'GD': 64.0, 'GA': 31.0, 'V': 23.0, 'CS': 55.0, 'CR': 24.0, 'DS': 110.0, 'CU': 29.0, 'SR': 38.0, 'UUP': 115.0, 'UUS': 117.0, 'TC': 43.0, 'KR': 36.0, 'SI': 14.0, 'SN': 50.0, 'SM': 62.0, 'UUT': 113.0, 'SC': 21.0, 'SB': 51.0, 'TA': 73.0, 'OS': 76.0, 'PU': 94.0, 'SE': 34.0, 'AC': 89.0, 'HS': 108.0, 'YB': 70.0, 'DB': 105.0, 'C': 6.0, 'HO': 67.0, 'DY': 66.0, 'HF': 72.0, 'HG': 80.0, 'HE': 2.0, 'PR': 59.0, 'PT': 78.0, 'LA': 57.0, 'F': 9.0, 'UUO': 118.0, 'LI': 3.0, 'PB': 82.0, 'TL': 81.0, 'TM': 69.0, 'LR': 103.0, 'PD': 46.0, 'TI': 22.0, 'TE': 52.0, 'TB': 65.0, 'PO': 84.0, 'PM': 61.0, 'ZN': 30.0, 'AG': 47.0, 'NI': 28.0, 'I': 53.0, 'K': 19.0, 'IR': 77.0, 'AM': 95.0, 'AL': 13.0, 'O': 8.0, 'S': 16.0, 'AR': 18.0, 'AU': 79.0, 'AT': 85.0, 'W': 74.0, 'IN': 49.0, 'Y': 39.0, 'CD': 48.0, 'ZR': 40.0, 'ER': 68.0, 'MD': 101.0, 'MG': 12.0, 'PA': 91.0, 'SG': 106.0, 'MO': 42.0, 'MN': 25.0, 'AS': 33.0, 'MT': 109.0, 'U': 92.0, 'XE': 54.0}

#write out put the headers - all the commands for GAMESS + ssbp
#functional = M06-2X - DFTTYP=M06-2X
f = open(output, 'w');
f.write(''' $CONTRL SCFTYP=RHF RUNTYP=MD COORD=UNIQUE
    DFTTYP=CAMB3LYP MAXIT=200 ICHARG=0 MULT=1 $END
 $MD KEVERY=10 PROD=.T. NVTNH=2 MBT=.T. MBR=.T. 
    BATHT=298 RSTEMP=.T. DTEMP=25 NSTEPS=50000
    SSBP=.T. SFORCE=1.0 DROFF='''+str(ssbpRadius)+''' $END
 $DFT DC=.F. $END
 $SYSTEM MWORDS=1000 MEMDDI=1000 $END
 $SCF DIRSCF=.T. $END
 $BASIS GBASIS=N31 NGAUSS=6 NDFUNC=2 NPFUNC=1 
    DIFFS=.TRUE. POLAR=POPN31 $END
 $DATA\n'''+ 'MD INPUT for' +input+'\nC1 1\n''')

#geometry
with open(input) as f1:
    #read by line
    #readlines if okay to use bc xyz is not too big
    lines = f1.readlines()
    #enumerate gets data in line - line and line index - n
    for n, line in enumerate(lines):
        #take all solute molecules (in range of 2 (line 3 where packmol starts) to num+2)
        #it's num+2 bc the range will go to num+1
        if n == 2:
            print 'Now Writing Solute:\n'
        if n in range(2,numberofSoluteAtoms+2):
            lineSplit=line.split();
            lineSplit.insert(1,str(atomicNumber[lineSplit[0]]))
            #convert coordinates to 10 decimals (add zeros if need be)
            for index in [2,3,4]:
                lineSplit[index]=float(lineSplit[index])
                lineSplit[index]=format(lineSplit[index],'.10f')
                grandString=lineSplit[0]+'\t'+lineSplit[1]+'\t'+lineSplit[2] + '\t'+lineSplit[3]+'\t'+lineSplit[4]+'\n';
            f.write(grandString)
            print grandString
        if n == numberofSoluteAtoms+2:
            f.write(' $END\n\n $EFRAG\nCOORD=CART  POSITION=OPTIMIZE\n')
            print 'Now Writing Solvent:\n'
        #now start doing solvent - (need to add fragment number and atom labels)
        startPointOfSolvent=numberofSoluteAtoms+2
        if n in range(startPointOfSolvent, startPointOfSolvent+numberOfAllSolventsAtoms+1):
            #atomlabel = O1, H2, H3 from O, H, H
            if atomLabel%numberofSoventAtoms==1:
                grandString='FRAGNAME=H2ODFT ! '+str(fragmentNumber)+'\n'
                f.write(grandString)
                print grandString
                fragmentNumber+=1;
                atomLabel%=numberofSoventAtoms
            lineSplit=line.split();
            lineSplit.insert(1,str(atomLabel))
            atomLabel+=1
            #convert coordinates to 10 decimals (add zeros if need be)
            for index in [2,3,4]:
                lineSplit[index]=float(lineSplit[index])
                lineSplit[index]=format(lineSplit[index],'.10f')
            grandString=' '+lineSplit[0]+lineSplit[1]+'\t'+lineSplit[2] + '\t'+lineSplit[3]+'\t'+lineSplit[4]+'\n';
            f.write(grandString)
            print grandString
    #close the inp with $END
    f.write(' $END\n')
###############################################################