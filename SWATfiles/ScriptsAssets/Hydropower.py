import pandas as pd
import numpy as np

def resRelease(file, dates):
    f = open(file,'r')
    f_content = f.readlines()
    f.close()
    
    # gibe i
    numFlowDays= len(dates)
    flowInGI = np.zeros(numFlowDays)
    flowOutGI = np.zeros(numFlowDays)
    resVolGI = np.zeros(numFlowDays)
    
    flowInGIII = np.zeros(numFlowDays)
    flowOutGIII = np.zeros(numFlowDays)
    resVolGIII = np.zeros(numFlowDays)
    
    flowInK = np.zeros(numFlowDays)
    flowOutK = np.zeros(numFlowDays)
    resVolK = np.zeros(numFlowDays)
    
    numSubB = 3
    flowSubBGI = 1
    flowSubBGIII = 2
    flowSubBK = 3
    
    for i in range(numFlowDays):
        gi = f_content[numSubB*i + flowSubBGI + 8]
        giii = f_content[numSubB*i + flowSubBGIII + 8]
        k = f_content[numSubB*i + flowSubBK + 8]
        
        resVolGI[i] = gi[20:32] 
        flowInGI[i] = gi[32:43]
        flowOutGI[i] = gi[44:55]

        resVolGIII[i] = giii[20:32] 
        flowInGIII[i] = giii[32:43]
        flowOutGIII[i] = giii[44:55]

        resVolK[i] = k[20:32] 
        flowInK[i] = k[32:43]
        flowOutK[i] = k[44:55]
        
    gi_d = {'dates': dates, 'volume': resVolGI, 'flowIn': flowInGI, 'flowOut': flowOutGI}
    giii_d = {'dates': dates, 'volume': resVolGIII, 'flowIn': flowInGIII, 'flowOut': flowOutGIII}
    k_d = {'dates': dates, 'volume': resVolK, 'flowIn': flowInK, 'flowOut': flowOutK}
    
    gi_df = pd.DataFrame(gi_d)
    giii_df = pd.DataFrame(giii_d)
    k_df = pd.DataFrame(k_d)

    return gi_df, giii_df, k_df


def levelToStorage(txtFile, df):
    lsv = pd.read_csv(txtFile, sep=' ',header=None)
    level = lsv.values[0].astype(np.float)
    storages = lsv.values[2].astype(np.float)
    df['head'] = np.interp(df.volume, storages, level)
    df['head'] = df['head'].shift(1) # SWAT reports end of day, so we need prior day info
    return df 

def DamHydro(df, effic):
    df['hyd'] = df[['flowOut', 'qMax']].apply(np.min,axis=1) * df['head'] * effic * 9.81 / 1000 
    return df

def calcHydropower(file, dates):
    gi, giii, k = resRelease(file, dates)
    
    GibeI = levelToStorage('lsv_GibeI.txt', gi)
    GibeIII = levelToStorage('lsv_GibeIII.txt', giii)
    Koysha = levelToStorage('lsv_Koysha.txt', k)

    # turbine capacity
    GibeI['qMax'] = 3*34 
    GibeIII['qMax'] = 10*95
    Koysha['qMax']= 8*192

    # individual dam hydropower - reservoirs (GI, GIII, K)
    effic = 0.8 
    GibeI = DamHydro(GibeI, effic)
    GibeIII  = DamHydro(GibeIII, effic)
    Koysha = DamHydro(Koysha, effic)
    
    # Gibe II 
    h_GII = 505 
    qMax_GII = 4*25.4
    GibeII = pd.DataFrame({'q_GI':GibeI.flowOut})
    GibeII['qMax_GII'] = qMax_GII
    GibeII['release'] = GibeII[['q_GI','qMax_GII']].apply(np.min,axis=1)
    GibeII['hyd'] = GibeII['release'] * h_GII * effic * 9.81 / 1000 

    hydro = GibeI.hyd + GibeII.hyd + GibeIII.hyd + Koysha.hyd 

    hydropower_ts = pd.DataFrame({'date':dates, 'year': dates.year, 'hydropower':hydro})
    return hydropower_ts