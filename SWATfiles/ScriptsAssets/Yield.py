import numpy as np
import pandas as pd 

def calcYld(file, dates):
    # open files 
    hru_s1 = []
    hru_s2 = []
    hru_s3 = []
    hru_c1 = []
    hru_c2 = []
    f = open(file, 'r')
    for line in f:
        if line[10:19] == '000240019':
            hru_s1.append(line)
        elif line[10:19] == '000240020':
            hru_s2.append(line)
        elif line[10:19] == '000240021':
            hru_s3.append(line)
        elif line[10:19] == '000250019':
            hru_c1.append(line)
        elif line[10:19] == '000250020':
            hru_c2.append(line)

    f.close()
    
    # sugarcane hrus 
    yld_s1 = np.zeros(len(hru_s1))
    yld_s2 = np.zeros(len(hru_s2))
    yld_s3 = np.zeros(len(hru_s3))
    
    # cotton hrus 
    yld_c1 = np.zeros(len(hru_c1))
    yld_c2 = np.zeros(len(hru_c2))

    # get yield values and area values
    for i in range(len(hru_s1)):
        yld_s1[i] = hru_s1[i][694:702]
        yld_s2[i] = hru_s2[i][694:702]
        yld_s3[i] = hru_s3[i][694:702]
        yld_c1[i] = hru_c1[i][694:702]
        yld_c2[i] = hru_c2[i][694:702]
        
        if i == 0:
            area_s1 = float(hru_s1[i][34:44]) / 0.01
            area_s2 = float(hru_s2[i][34:44]) / 0.01
            area_s3 = float(hru_s3[i][34:44]) / 0.01
            area_c1 = float(hru_c1[i][34:44]) / 0.01
            area_c2 = float(hru_c2[i][34:44]) / 0.01
            
            
    # make dataframe 
    sugc = pd.DataFrame({'s1_kg':yld_s1*area_s1, 's2_kg':yld_s2*area_s2, 's3_kg':yld_s3*area_s3, 'year':dates.year})
    sugc = sugc.groupby("year").sum()
    cotp = pd.DataFrame({'c1_kg':yld_c1*area_c1, 'c2_kg':yld_c2*area_c2, 'year':dates.year})
    cotp = cotp.groupby("year").sum()
    return sugc, cotp