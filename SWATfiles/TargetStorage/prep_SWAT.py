# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 11:00:02 2021

@author: Sarah

rewrite mgt file 
rewrite res file
for existing SWAT reservoir operations
"""

### PACKAGES ##################################################################
import os
import numpy as np

### READ IN FILES ############################################################

def writeArrays(var_file):
    # initial definitions 
    nvar = 44
    with open(var_file) as f:
        refset = [line.rstrip() for line in f]
    # refset = np.loadtxt(var_file)

    # separate -- check all these
    irr = refset[0:5]
    gi = refset[5:18]
    giii = refset[18:31]
    k = refset[31::]

    return irr, gi, giii, k
    

def replace_line(file_name, line_num, text):
    with open(file_name) as f:
        l = f.readlines()
        l[line_num] = text

    out = open(file_name, 'w')
    out.writelines(l)
    out.close()
    
    
def replaceIrrigation(irr):
    irrSugc = '  1  1          10    1   1 24      0.10000   0.60     0.60000 0.00                        1\n'
    irrCotp = '  1  1          10    1   1 25      0.10000   0.60     0.60000 0.00                        1\n'
    
    # read in parameters from Borg 
    lines = [float(i) for i in irr]
    
    # right number of decimal places 
    for i in range(4):
        lines[i] = format(lines[i], '.5f')
    
    # round wstrs_id value 
    if lines[4] < 1.5:
        lines[4] = 1
    else:
        lines[4] = 2
        
    if len(lines[0]) > 11:
        lines[0] = lines[0][0:11]
        
        
    # build new lines
    lenAutoSugc = 11-len(lines[0])
    lenAutoCotp = 11-len(lines[2])
    lenMxSugc = 10-len(lines[1])
    lenMxCotp = 10-len(lines[3])
    irrSugcRep = irrSugc[0:22] + str(lines[4]) + irrSugc[23:32] + ' ' * lenAutoSugc + lines[0] + irrSugc[43:52] + ' '*lenMxSugc + lines[1] + irrSugc[62:] 
    irrCotpRep = irrCotp[0:22] + str(lines[4]) + irrCotp[23:32] + ' ' * lenAutoCotp + lines[2] + irrCotp[43:52] + ' '*lenMxCotp + lines[3] + irrCotp[62:] 
    replace_line('000240019.mgt', 30, irrSugcRep)
    replace_line('000240020.mgt', 30, irrSugcRep)
    replace_line('000240021.mgt', 30, irrSugcRep)
    replace_line('000250020.mgt', 30, irrCotpRep)
    replace_line('000250019.mgt', 30, irrCotpRep)

def replaceRes(res, res_name):
    for i in range(len(res) - 1):
        res[i] = format(float(res[i]), '.1f')
    ndtargr = str(int(float(res[-1])))


    if res_name == "gi":
        res_file = "000100000.res"
    elif res_name == "giii":
        res_file = "000130000.res"
    elif res_name == "k":
        res_file = "000170000.res"
    else:
        print("Reservoir name error: input 'gi', 'giii', or 'k'.")

    # each gets 10 spaces total
    jan_jun = str()
    jul_dec = str()
    for i in range(6):
        jan_jun = jan_jun + ' '*(10 - len(res[i])) + res[i]  
        jul_dec = jul_dec + ' '*(10 - len(res[i + 6])) + res[i+6]
    jan_jun = jan_jun + '\n'
    jul_dec = jul_dec + '\n'
    replace_line(res_file, 28, jan_jun) 
    replace_line(res_file, 30, jul_dec)  

    # ndtargr 
    ndtargr_str = ' '*(16 - len(ndtargr)) + ndtargr + '    | NDTARGR : Number of days to reach target storage from current reservoir storage\n'
    replace_line(res_file, 26, ndtargr_str)




irr, gi, giii, k = writeArrays("vars_file.txt")
replaceIrrigation(irr)
for item, name in zip([gi, giii, k],["gi","giii","k"]):
    replaceRes(item, name)
