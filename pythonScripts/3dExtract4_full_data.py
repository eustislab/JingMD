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
FoundFirstGeometry=False
foundTime=False
foundPE=False
time=''
energy='0'
grandString=''
lineBwTimeAndEnergy=0
lineBwTimeAndGeometry=0
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
#for finding PE
lineCountFromTime=0
#for printing time
def printAndReturnTime (thisLine):
    lineComponents=thisLine.split();
    timeString=str(lineComponents[3]);
    #get rid off .00
    timeString=timeString[:-3]
    print "Analyzing t = "+timeString+" fsec\n"
    return timeString

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

def shouldCollectTime(line):
    #only check if collection is in progress
    if ' *** AT T=' in line:
        return True;
    else:
        return False;

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
        
def shouldStartCollectGeometry(line,reference,currentLine):
    #check if line bw time and geometry is known - reference
    if reference>0:
        if currentLine==reference:
            return True
        else:
            return False
    #if not then it needs to be found by searching for the string TEMPER...
    elif reference==0:
        if ' QM ATOM ' in line:
            reference=int(currentLine)
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
    #find out if we have found the first geoetry
    if not FoundFirstGeometry: 
        #if not then find it
        if shouldCollect():
            #split line
            lineSplit=line.split()
            atomCount+=1;
            #append to molList
            molList.append(lineSplit)
            time=str(0)
            if shouldWrite():
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
                grandString=grandString+str(atomCount)+'\n'+str(timeCount)+'\tfs\t'+str(energy)+' KCAL/MOL\n'
                f.write(grandString)
                #loop tho molList to add data - molList = [['N','1','1','1'],['C'...],... ] And element = ['N','1','1','1']
                for element in molList:
                    #loop through element in molList data = 'N','1','1','1'
                    for data in element:
                        #add to grandString and don't forget tab, return
                        f.write(data+'\t')
                    #end one element with a return
                    f.write('\n')
                #reset all values after writing
                atomCount=0;
                molList=[]
                collectionStarted=False;
                FoundFirstGeometry=True;
                timeCount+=1
                grandString=''
        if ' QM ATOM COORDINATES (ANG)' in line:
            collectionStarted=True

    if FoundFirstGeometry: 
        if not foundTime:
            if shouldCollectTime(line):
                newTime=printAndReturnTime(line);
                if int(time)>=int(newTime):
                	print 'there is a duplication at '+time+' and '+newTime +' ignoring new values'
                else:
                	time=str(newTime)
                	foundTime=True;
                if time=='0.00':
                    foundTime=False
                    grandString=''
        elif not foundPE:
            if shouldCollectPE(line,lineBwTimeAndEnergy,lineCountFromTime):
                #split line using space - sample(     POT  ENERGY      =     -1.804578585E+05 KCAL/MOL)
                #this will be split to [..., '=', '-1.804578585E+05'...] -time = element 4
                lineComponents=line.split();
                energy=str(lineComponents[3])
                foundPE=True
        elif shouldCollect():
            #split line
            lineSplit=line.split()
            atomCount+=1;
            #append to molList
            molList.append(lineSplit)
            if shouldWrite():
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
                grandString=grandString+str(atomCount)+'\n'+str(time)+'\tfs\t'+str(energy)+' KCAL/MOL\n'
                f.write(grandString)
                #loop tho molList to add data - molList = [['N','1','1','1'],['C'...],... ] And element = ['N','1','1','1']
                for element in molList:
                    #loop through element in molList data = 'N','1','1','1'
                    for data in element:
                        #add to grandString and don't forget tab, return
                        f.write(data+'\t')
                    #end one element with a return
                    f.write('\n')
                #reset all values after writing
                atomCount=0;
                molList=[]
                collectionStarted=False;
                foundTime=False
                foundPE=False
                lineCountFromTime=0;
                grandString=''
                timeCount+=1
        elif shouldStartCollectGeometry(line,lineBwTimeAndGeometry,lineCountFromTime):
                collectionStarted=True
    lineCountFromTime+=1
f.close()
#sanity check
print 'Done. Extract ' + str(timeCount) + ' snapshots total.'
            