import sys

radiusInSolute=0.0
radiusInSolvent=0.0
avgX=0.0
avgY=0.0
avgZ=0.0
X=[]
Y=[]
Z=[]

callAs='\nCall function as: radiusDetermination.py input.log numberOfSoluteAtoms\n'
try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: '+callAs 
		sys.exit()
except IndexError:
    print '\n!!!Input command Error. Call function as: '+callAs 
    sys.exit()

try:
    input=str(sys.argv[1])
    numberofSoluteAtoms=int(sys.argv[2])
except IndexError:
    print '\n!!!Input command Error. Call function as: ' +callAs
    sys.exit()
    
#open input
f1=open(input)
#enumerate gets data in line - line and line index - n
lineNumber=0
for line in f1:
	lineNumber+=1
	if lineNumber>2:
		lineSplit=line.split()
		X.append(float(lineSplit[1]))
		Y.append(float(lineSplit[2]))
		Z.append(float(lineSplit[3]))
	
size=len(X)
avgX=sum(X[:numberofSoluteAtoms-1])/numberofSoluteAtoms
avgY=sum(Y[:numberofSoluteAtoms-1])/numberofSoluteAtoms
avgZ=sum(Z[:numberofSoluteAtoms-1])/numberofSoluteAtoms
print avgX
print avgY
print avgZ
for i in range(0,size):
		d=((X[i]-avgX)**2+(Y[i]-avgY)**2+(Z[i]-avgZ)**2)**0.5
		if i<numberofSoluteAtoms:
			if radiusInSolute<d:
				radiusInSolute=d
		else:
			if radiusInSolvent<d:
				radiusInSolvent=d

#radius should be a little bit larger than the two combined
radiusInSolute=radiusInSolute
radiusInSolvent=radiusInSolvent
ssbpRadius=radiusInSolute+radiusInSolvent+3

print '\n'
print 'Radius in solute is:\t'+str(radiusInSolute)
print 'Radius in solvent is:\t'+str(radiusInSolvent)
print 'ssbp Radius should be:\t'+str(ssbpRadius)
print '\n'