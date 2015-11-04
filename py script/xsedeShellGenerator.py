import os
import sys

input=str(sys.argv[1])
path = os.getcwd()
inputPath=path+'/'+input


allspark = os.listdir(inputPath)


f = open('megalo_'+input+'.txt','w')
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

rungms '''+outputName[:-3]+'''.inp 00 24 >& ~/out/'''+outputName[:-3]+'''.out'''
		f1.write(grandString)
		f1.close()
		f.write('sbatch '+outputName+'\n')