###########################################################
###This version is created to solve memory error when   ###
###used with large log file (5Gb up). The slow speed is ###
### undesirable but it's what it is now. The problem is ###
###avoided by looping in open instead of readlines()    ###
###########################################################
import os as os
import sys

#Call as 3dExtract.py inputfile #ofsoluteAtom #ofsolventAtom #ofsoluteMolecules
try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: 3dExtract.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules   \n' 
		sys.exit()
except IndexError:
    print '\n!!!Input command Error. Call function as: 3dExtract.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules   \n' 
    sys.exit()

try:
    input=str(sys.argv[1])
    numberofSoluteAtoms=int(sys.argv[2])
    numberofSoventAtoms=int(sys.argv[3])
    numberOfSolventMolecules=int(sys.argv[4])
except IndexError:
    print '\n!!!Input command Error. Call function as: 3dExtract.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules \n' 
    sys.exit()
    

numberOfAllSolventsAtoms=numberofSoventAtoms*numberOfSolventMolecules
previousGrandString=''
collectionStarted=False
time=''
#1 is for cartesian line, then 1 in 3(n+1) is for fragment H2O line 
numberOfLinesToBecollected=numberofSoluteAtoms+1+numberOfSolventMolecules*(numberofSoventAtoms+1)

if input.endswith('.log'):
    output = str(input[:-4])+'.xyz'
else:
    output=str(input)
#number of molecules so far
timeCount=0
#total number of atoms (solute + solvent) - used later in checking if file is complete
atomCount=0
#define functions here
lineSinceTimeIsFound=0;
#do an input of solvent, solute atoms 
molList=[]
def printTime (thisLine):
    lineComponents=thisLine.split();
    timeString=str(lineComponents[3]);
    print "Analyzing t = "+timeString+" fsec\n"
def shouldCollect():
    #only check if collection is in progress
    if collectionStarted:
        #from first solute atom to the last fragment atom
        if (atomCount>=0 and atomCount<numberOfLinesToBecollected):
            return True;
        else:
            return False;
    else:
        return False;
def shouldWrite():
    #only check if collection is in progress
    if collectionStarted:
        #solute
        if (atomCount==numberOfLinesToBecollected):
            return True;
        else:
            return False;
    else:
        return False;
def moleculeIsNotADuplication(currentMoleculeToBeWritten):
    halfSize=int(len(previousGrandString)/2)
    threeQuartersSize=int(len(previousGrandString)*3/4)
    if previousGrandString=='':
        return True;
    if (currentMoleculeToBeWritten[halfSize:threeQuartersSize] not in previousGrandString[halfSize-1:threeQuartersSize+1]):
        return True;
    else:
        return False;
#clear output.xyz
f = open(output, 'w');
f.write('')
#open input
f1=open(input)
#enumerate gets data in line - line and line index - n
for line in f1:
    #this keyword is usually before coordinate
    grandString=''
    #find out if collection is needed            
    if shouldCollect():
        #split line
        lineSplit=line.split()
        atomCount+=1;
        #append to molList
        molList.append(lineSplit)
    elif ' QM ATOM COORDINATES (ANG)' in line:
        collectionStarted=True
    elif  ' *** AT T=' in line:
        time=str(line)
        printTime(line);
        
    if (shouldWrite()):
        atomCount=atomCount-(numberOfSolventMolecules+1);
        #for loop through a ***COPY*** of molList and delete some element from molList!
        #if you don't realize six asterisk then you should go back up - we do this so we can remove element along the way without messing up the index
        for line in list(molList):
            #if line has 4 elements then it's a coordinate from solvent fragment - we have to drop number behind atom - O1 to O
            if len (line) == 4:
                #store string
                oldString =  line[0]
                #replacement string
                newString=''
                #loop to check if it's a alphabet or not
                for character in range(len(oldString)):
                    #do substring of 1 character
                    subString = oldString[character:character+1]
                    #check if it's an alphabet - yes? then add to newString
                    if subString.isalpha():
                        newString = newString + subString
                #replace 'O1' with 'O'
                line[0]=newString
            #if it's 5 then it's solute coordinate - we have to get rid of atomic number behind atomic representation
            elif len(line) == 5:
                # 'N 7.0 ...' will become 'N ...' 
                del line[1]
            #the rest are crap - just remove it out of the line
            else:
                #there's a reason why this is remove - not del - since we are iterating if we delete using index we are gonna be screwed
                molList.remove(line)
        #xyz file has a format that we need atomCount at the top followed by snapshot number(timeCount) on the next line before adding any coordinates
        grandString=grandString+str(atomCount)+'\n'+str(timeCount)+'\n'
        #loop tho molList to add data - molList = [['N','1','1','1'],['C'...],... ] And element = ['N','1','1','1']
        for element in molList:
            #loop through element in molList data = 'N','1','1','1'
            for data in element:
                #add to grandString and don't forget tab, return
                grandString=grandString+data+'\t'
            #end one screenshot with a return
            grandString=grandString+'\n'
        #open animate.xyz for writing
        if moleculeIsNotADuplication(grandString):                 
            with open(output, 'a') as f:
                f.write(grandString)
                #add one to timeCount because we already write grandString
                timeCount=timeCount+1
        atomCount=0;
        molList=[]
        collectionStarted=False;
        previousGrandString=str(grandString)
f.close()
print 'Done. Extract ' + str(timeCount) + ' snapshots total.'

totalLineInOneSet=numberofSoluteAtoms+numberofSoventAtoms*numberOfSolventMolecules+2
totalLineToBeCollected=totalLineInOneSet-2
output2=str(output[:-4])+'.csv'
f=open(output, 'r')
f2 = open(output2, 'w')
lines=f.readlines()
counter=0
for n, line in enumerate(lines):
    if n%totalLineInOneSet==0:
        f2.write(str(counter)+', ')
    elif (n%totalLineInOneSet!=1):
        lineSplit=line.split()
        lineSplit.pop(0)
        for element in lineSplit:
            f2.write(element+', ')
    if n%totalLineInOneSet==totalLineInOneSet-1:
        lineSplit=line.split()
        lineSplit.pop(0)
        for n, element in enumerate(lineSplit):
            if n!=int(len(lineSplit))-1:
                f2.write(element+',')
            else:
                f2.write(element+'\n')
                counter+=10
            