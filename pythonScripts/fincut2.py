###########################################################
### This script create a folder of inp for TDDFT        ###
###########################################################

import os
import sys

#call as fincut.py input.log startTime stopTime timePerFrame
#this will run from starting startTime+timePerFrame to stopTime
#for example 15010-25000 if input is 15000, 25000

#this dict is for generating atomic number from Acronym
atomicNumber={'LV': 116.0, 'BE': 4.0, 'FR': 87.0, 'BA': 56.0, 'BH': 107.0, 'BI': 83.0, 'BK': 97.0, 'EU': 63.0, 'FE': 26.0, 'BR': 35.0, 'ES': 99.0, 'FL': 114.0, 'FM': 100.0, 'RG': 111.0, 'RU': 44.0, 'NO': 102.0, 'NA': 11.0, 'NB': 41.0, 'ND': 60.0, 'NE': 10.0, 'RE': 75.0, 'RF': 104.0, 'LU': 71.0, 'RA': 88.0, 'RB': 37.0, 'NP': 93.0, 'RN': 86.0, 'RH': 45.0, 'B': 5.0, 'CO': 27.0, 'TH': 90.0, 'CM': 96.0, 'CL': 17.0, 'H': 1.0, 'CA': 20.0, 'CF': 98.0, 'CE': 58.0, 'N': 7.0, 'CN': 112.0, 'P': 15.0, 'GE': 32.0, 'GD': 64.0, 'GA': 31.0, 'V': 23.0, 'CS': 55.0, 'CR': 24.0, 'DS': 110.0, 'CU': 29.0, 'SR': 38.0, 'UUP': 115.0, 'UUS': 117.0, 'TC': 43.0, 'KR': 36.0, 'SI': 14.0, 'SN': 50.0, 'SM': 62.0, 'UUT': 113.0, 'SC': 21.0, 'SB': 51.0, 'TA': 73.0, 'OS': 76.0, 'PU': 94.0, 'SE': 34.0, 'AC': 89.0, 'HS': 108.0, 'YB': 70.0, 'DB': 105.0, 'C': 6.0, 'HO': 67.0, 'DY': 66.0, 'HF': 72.0, 'HG': 80.0, 'HE': 2.0, 'PR': 59.0, 'PT': 78.0, 'LA': 57.0, 'F': 9.0, 'UUO': 118.0, 'LI': 3.0, 'PB': 82.0, 'TL': 81.0, 'TM': 69.0, 'LR': 103.0, 'PD': 46.0, 'TI': 22.0, 'TE': 52.0, 'TB': 65.0, 'PO': 84.0, 'PM': 61.0, 'ZN': 30.0, 'AG': 47.0, 'NI': 28.0, 'I': 53.0, 'K': 19.0, 'IR': 77.0, 'AM': 95.0, 'AL': 13.0, 'O': 8.0, 'S': 16.0, 'AR': 18.0, 'AU': 79.0, 'AT': 85.0, 'W': 74.0, 'IN': 49.0, 'Y': 39.0, 'CD': 48.0, 'ZR': 40.0, 'ER': 68.0, 'MD': 101.0, 'MG': 12.0, 'PA': 91.0, 'SG': 106.0, 'MO': 42.0, 'MN': 25.0, 'AS': 33.0, 'MT': 109.0, 'U': 92.0, 'XE': 54.0}

#if not sure use ? to ask
try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: fincut.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules startTime stopTime timePerFrame\n' 
		sys.exit()
except IndexError:
    print '\n!!!Input command Error. Call function as: fincut.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules startTime stopTime timePerFrame\n' 
    sys.exit()

#Call as fincut.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules startTime stopTime timePerFrame
try:
    input=str(sys.argv[1])
    numberOfSoluteAtoms=int(sys.argv[2])
    numberOfSolventAtoms=int(sys.argv[3])
    numberOfSolventMolecules=int(sys.argv[4])
    startTime =int(sys.argv[5])
    stopTime =int(sys.argv[6])
    timePerFrame=int(sys.argv[7])
except IndexError:
    print '\n!!!Input command Error. Call function as: fincut.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules startTime stopTime timePerFrame\n' 
    sys.exit()

#should collect data when 1) time within interval specified
#2) they are x y z line - not line 1 and 2
def shouldCollect(numberOfLine):
    frame=int(numberOfLine/totalNumberOfLineInOneSet)
    time=frame*timePerFrame
    #if within range
    if time>startTime and time<=stopTime:
        #0 and 1 (line 1 and 2) in each frame in xyz are not useful
        if numberOfLine%totalNumberOfLineInOneSet!=0 and numberOfLine%totalNumberOfLineInOneSet!=1:
            return True
        else:
            return False
    else:
        return False

#condition for writing to each inp
def shouldWrite(numberOfLine):
    #should write when last line of a frame is read
    if numberOfLine%totalNumberOfLineInOneSet==totalNumberOfLineInOneSet-1 :
        return True
    else:
        return False

#write FRAGNAME=H2ODFT ! 1 
def shouldWriteFragmentHeader(numberOfLineInSolvent):
    #should write before writing geometry of solvent molecules
    if numberOfLineInSolvent%numberOfSolventAtoms==0 :
        return True
    else:
        return False

#create format of GAMESS inp
def insertAtomicNumberInto(line):
                lineSplit=line.split()
                lineSplit.insert(1,str(atomicNumber[lineSplit[0]]))
                return lineSplit[0]+'\t'+lineSplit[1]+'\t'+lineSplit[2]+'\t'+lineSplit[3]+'\t'+lineSplit[4]+'\n'
#create format of GAMESS inp O -> O1, H-> H2...
def insertCountsInto(line, count):
                lineSplit=line.split()
                lineSplit[0]=lineSplit[0]+str(count)
                return lineSplit[0]+'\t'+lineSplit[1]+'\t'+lineSplit[2]+'\t'+lineSplit[3]+'\n'

#even tho input is received written in .log - it will ultimately use .xyz created by 3dExtract for efficiency
#this can be confusing - room for improvement
if input.endswith('.log'):
    input = input[:-4]

#Path for storing input files
path = os.getcwd()
inputPath=path+'/'+input+'InputFiles'
#create folders if not already done
if not os.path.exists(inputPath): os.makedirs(inputPath)

#initiate variables
grandString=[]
lineNumber=0
numberOfAllSolventsAtoms=numberOfSolventAtoms*numberOfSolventMolecules
totalNumberOfAtoms=numberOfSoluteAtoms+numberOfAllSolventsAtoms
totalNumberOfLineInOneSet=totalNumberOfAtoms+2

#if no xyz in folder - ask for it
    #if no 3dExtract.py - print...
    #if there is, call it from here + print s'th
#else create one?
#if there is, then proceed 
#this is very confusing - if there is xyz but it's not updated when it's of no use - room for improvement

#open input.xyz
try: 
    f=open(input+'.xyz')
except IOError:
    print '\nThere is currently no xyz file named '+input
    print 'trying to call 3dExtract'
    try:
        os.system('python 3dExtract4.py'+' '+input+'.log'+' '+str(numberOfSoluteAtoms)+' '+str(numberOfSolventAtoms)+' '+str(numberOfSolventMolecules))
    except IOError:
        print '\n  Error. There is no 3dExtract to call. Try copying 3dExtract here. \n'
        print 'Process terminated abnormally'
        sys.exit()
    f=open(input+'.xyz')
    
#since we are reading from xyz - using readlines() is okay
numberOfAllAtoms=int(f.readline().strip())
#enumerate gets data in line - line and line index - n
for line in f:
    lineNumber+=1
    #check if the line should be writen
    if shouldCollect(lineNumber):
        grandString.append(line)
        #if about to write -create file with this name
        if shouldWrite(lineNumber):
            frame=int(lineNumber/totalNumberOfLineInOneSet)
            time=frame*timePerFrame
            f1 = open(inputPath+'/'+input+'_'+str(time)+'.inp','w')
            #write header
            headerString=""" $CONTRL SCFTYP=RHF TDDFT=EXCITE DFTTYP=CAMB3LYP RUNTYP=ENERGY                     
       ICHARG=0 MULT=1 COORD=UNIQUE MAXIT=200 $END   
 !TDDFT requires lots of memory space                                      
 $SYSTEM MWORDS=200 MEMDDI=250 $END
 $SCF DIRSCF=.T. $END                                                         
 $TDDFT NSTATE=5 TPA=.f. $END   
 $BASIS GBASIS=N311 NGAUSS=6 NDFUNC=2 NPFUNC=1 
       DIFFSP=.TRUE. DIFFS=.TRUE. POLAR=POPN311 $END             
 $DATA\n"""+input+' at t= '+str(time)+'\nC1 1\n'
            print 'Making input file for 'input+' at t= '+str(time)
            #write the header
            f1.write(headerString)
            #write one line by one - before writing we need to add atomic number in using the function defined above
            for eachLine in grandString[:numberOfSoluteAtoms]:
                eachLine=insertAtomicNumberInto(eachLine)
                f1.write (eachLine)
            #end solute and go to solvent
            stringBwSoluteAndSolvent=""" $END\n\n $EFRAG\nCOORD=CART  POSITION=OPTIMIZE \n"""
            f1.write(stringBwSoluteAndSolvent)
            #write fragments
            #for iteration
            i=0
            for numberOfLineWithInSolvents, eachLine in enumerate(grandString[numberOfSoluteAtoms:]):
            	#is header needed - if so write
                if shouldWriteFragmentHeader(numberOfLineWithInSolvents):
                    fragmentsNumber=numberOfLineWithInSolvents/numberOfSolventAtoms+1
                    f1.write("FRAGNAME=H2ODFT ! "+str(fragmentsNumber)+'\n')
                #write each line in fragments
                atomNumberInFragments=i%numberOfSolventAtoms+1
                eachLine=insertCountsInto(eachLine, atomNumberInFragments)
                f1.write (eachLine)
                i+=1
            #close and reset
            f1.write (" $END\n")
            grandString=[]
            f1.close()

#create megaio for gmssub input
allFiles = os.listdir(inputPath)
program = 'gmssub'
processors = '32'

#create the write file - like gmssub aniline32.inp aniline32.log -l 10g=true
f = open('megaio_'+input+'.txt','w')
#write each item
for item in allFiles:
	#for GAMESS output naming
    outputName=str(item)[:-4]+'.log'
    f.write(program + ' %s '%item + processors +' '+outputName+' -l 10g=true\n')
f.close()