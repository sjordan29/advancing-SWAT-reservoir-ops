# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 11:00:02 2021

@author: Sarah

rearrange arrays from optimization to an irr file, var file, and c, r, w arrays 
change irrigation values based on values from optimization 
"""

### PACKAGES ##################################################################
import os
import numpy as np

### READ IN FILES ############################################################

def writeArrays(var_file):
    # initial definitions 
    M = 5 # number of inputs (reservoirs + 2)
    K = 3 # number of outputs (reservoirs)
    N = 9 # number of RBFs
    
    nvar = 5 + K + N*(2*M+K) # number of decision variables
    with open(var_file) as f:
        refset = [line.rstrip() for line in f]
    # refset = np.loadtxt(var_file)

    var = refset[5:nvar]
    irr = refset[0:5]
    var2 = var[K::]

    C = np.zeros([M,N])
    R = np.zeros([M,N])
    W = np.zeros([K,N])
    
    for n in range(N):
        for m in range(M):
            C[m,n] = var2[(2*M+K)*n + 2*m]
            R[m,n] = var2[(2*M+K)*n + 2*m + 1]
        for k in range(K):
            W[k,n] = var2[(2*M+K)*n + 2*M + k]
     
    
    np.savetxt('c.txt',C, fmt='%s')
    np.savetxt('r.txt',R,fmt='%s')
    np.savetxt('w.txt',W, fmt='%s')
    np.savetxt('var.txt',var, fmt='%s')
    np.savetxt('irr.txt', irr, fmt='%s')
    

def replace_line(file_name, line_num, text):
    with open(file_name) as f:
        l = f.readlines()
        l[line_num] = text

    # l = open(file_name, 'r').readlines()
    # l[line_num] = text
    # l.close()
    out = open(file_name, 'w')
    out.writelines(l)
    out.close()
    
    
def replaceIrrigation(textfile):
    irrSugc = '  1  1          10    1   1 24      0.10000   0.60     0.60000 0.00                        1\n'
    irrCotp = '  1  1          10    1   1 25      0.10000   0.60     0.60000 0.00                        1\n'
    
    # read in parameters from Borg 
    text_file = open(textfile, "r")
    lines = text_file.read().split('\n')
    lines = lines[0:5]
    lines = [float(i) for i in lines]
    text_file.close()
    
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

writeArrays("vars_file.txt")
replaceIrrigation("irr.txt")

