out32MDdata=csvread('aniline64_combinedInputFilesMD_data.csv')
S1 = out32MDdata(1:1000,2:3);
S2 = out32MDdata(1:1000,4:5);
S3 = out32MDdata(1:1000,6:7);
S4 = out32MDdata(1:1000,8:9);
S5 = out32MDdata(1:1000,10:11);
run('fitfn.m')
run('fitSn.m')