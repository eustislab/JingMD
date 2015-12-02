###########################################################
### 3dExtract pulls out geometries from MD run and make ###
### an xyz-movie file for inspection MD	progress     	###
###########################################################

import os as os
import sys

#for asking what the input in terminal should be
try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: 3dExtract.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules   \n' 
		sys.exit()
except IndexError:
    print '\n!!!Input command Error. Call function as: 3dExtract.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules   \n' 
    sys.exit()

#Call as 3dExtract.py inputfile #ofsoluteAtom #ofsolventAtom #ofsoluteMolecules
try:
    input=str(sys.argv[1])
    numberofSoluteAtoms=int(sys.argv[2])
    numberofSoventAtoms=int(sys.argv[3])
    numberOfSolventMolecules=int(sys.argv[4])
except IndexError:
    print '\n!!!Input command Error. Call function as: 3dExtract.py input.log numberOfSoluteAtoms numberofSolventAtoms numberOfSolventMolecules \n' 
    sys.exit()
if input.endswith('.log'):
    output = str(input[:-4])+'.xyz'
else:
    output=str(input)

numberOfAllSolventsAtoms=numberofSoventAtoms*numberOfSolventMolecules
#This is for comparing files to be written
previousGrandString=''
collectionStarted=False
time=''
#1 is for cartesian line (useless), then 1 in 3(n+1) is for fragment H2O line (also useless)
numberOfLinesToBecollected=numberofSoluteAtoms+1+numberOfSolventMolecules*(numberofSoventAtoms+1)


#number of molecules so far
timeCount=0
#total number of atoms (solute + solvent) - used later in checking if file is complete
atomCount=0
#define functions here
lineSinceTimeIsFound=0;
#do an input of solvent, solute atoms 
molList=[]
#for printing time
def printTime (thisLine):
    lineComponents=thisLine.split();
    timeString=str(lineComponents[3]);
    print "Analyzing t = "+timeString+" fsec\n"
#to determine if line should be collected - 
def shouldCollect():
    #only check if collection is in progress - if it is, then continue to finish collecting the lines
    #collectionStarted is determined when ' QM ATOM COORDINATES (ANG)'  is found
    if collectionStarted:
        #from first solute atom to the last fragment atom
        if (atomCount>=0 and atomCount<numberOfLinesToBecollected):
            return True;
        else:
            return False;
    else:
        return False;
# only write when atomCount==numberOfLinesToBecollected
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
        
#Even now I still don't understand why GAMESS duplicate system geometry for a step twice in the log file
#This is written to prevent duplication of geometry in the xyz-movie file
def moleculeIsNotADuplication(currentMoleculeToBeWritten):
	# to compare previously stored geometry and a new one is tricky bc each string has different lengths
	# there must be a better of doing this - note for possible place for improvement
	#current the speed is quite slow probably due to this step
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
#readlines() is eliminated because it creates a huge array and python cannot handle it when log file get very large
#using for line in... alleviate the burden on memory and actually speed up the process
for line in f1:
    #this keyword is usually before coordinate
    grandString=''
    #find out if checking for collectionStarted is needed            
    if shouldCollect():
        #split line
        lineSplit=line.split()
        atomCount+=1;
        #append to molList
        molList.append(lineSplit)
    # if this then start collecting
    elif ' QM ATOM COORDINATES (ANG)' in line:
        collectionStarted=True
    #lastly, if none of the above, then find and print time
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
        #this is for if we have an incomplete file or inconsistant number of atoms we should only use the one before and break for loop without appending to grandString
        if len(molList) != atomCount:
            print 'error'
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
        #reset all values after writing
        atomCount=0;
        molList=[]
        collectionStarted=False;
        previousGrandString=str(grandString)
f.close()
#sanity check
print 'Done. Extract ' + str(timeCount) + ' snapshots total.'
            