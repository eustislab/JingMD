###########################################################
### create sh files to run inp files on comet           ###
###########################################################

import os
import sys


#if you don't know then ask ?
try:
	if str(sys.argv[1])=='?':
		print '\nCall function as: xsedeShellGenerator.py inputDirectory\n' 
		sys.exit()
except IndexError:
    print '\n!!!Input command Error. Call function as: xsedeShellGenerator.py inputDirectory\n' 
    sys.exit()

#Call as xsedeShellGenerator.py inputDirectory
try:
    input=str(sys.argv[1])
except IndexError:
    print '\n!!!Input command Error. Call function as: xsedeShellGenerator.py inputDirectory\n' 
    sys.exit()

path = os.getcwd()
inputPath=path+'/'+input


allspark = os.listdir(inputPath)


f = open('megaio_'+input+'.txt','w')
for item in allspark:
	if not item.startswith('.') and os.path.isfile(os.path.join(inputPath, item)):
		outputName=str(item)[:-4]+'.sh'
		f1=open(inputPath+'/'+outputName, 'w')
		grandString='''#!/bin/bash
#SBATCH -p compute
#SBATCH -t 01:00:00
#SBATCH -o '''+outputName[:-3]+'''.out.%j
#SBATCH -e '''+outputName[:-3]+'''.error.%j
#SBATCH -J '''+outputName[:-3]+'''.inp
#SBATCH --nodes=1  
#SBATCH --ntasks-per-node=24  

module load gamess

export GAMESS_SCR=/scratch/$USER/$SLURM_JOBID

rungms '''+outputName[:-3]+'.inp 00 24 >& ~/'+input+'/'+input+'_out/'+outputName[:-3]+'.log'
		f1.write(grandString)
		f1.close()
		f.write('sbatch '+outputName+'\n')
