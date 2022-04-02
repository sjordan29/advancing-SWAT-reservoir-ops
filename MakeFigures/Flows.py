import numpy as np
import pandas as pd
import datetime 

pd.options.mode.chained_assignment = None

def datestdtojd (stddate):
    fmt='%Y-%m-%d'
    sdtdate = datetime.datetime.strptime(stddate, fmt)
    sdtdate = sdtdate.timetuple()
    jdate = sdtdate.tm_yday
    return(jdate)


def calcFloodRecession(filename, dates):
    f = open(filename,'r')
    f_content = f.readlines()
    f.close()
    
    # dates = pd.date_range(start="1989-01-01",end="2018-12-31", freq='d')

    # flow at delta is the flow into subbasin 27
    numFlowDays= len(dates)
    simulatedFlow = np.zeros(numFlowDays)
    numSubB = 27
    flowSubB = 24 # 
    for i in range(numFlowDays):
        y = f_content[numSubB*i+flowSubB+8]
        # simulatedFlow[i] = y[38:49]
        simulatedFlow[i] = y[50:62]

    jdates= []
    for item in dates:
        date_time = item.strftime("%Y-%m-%d")
        jd = datestdtojd(date_time)
        jdates.append(jd)

    df = pd.DataFrame({'date':dates,'year':dates.year,'doy':jdates,'month':dates.month, 'day':dates.day,'flow':simulatedFlow})
    return df

def calcEnvFlow(filename, dates):
    f = open(filename,'r')
    f_content = f.readlines()
    f.close()
    
    # dates = pd.date_range(start="1989-01-01",end="2018-12-31", freq='d')

    # flow at delta is the flow into subbasin 27
    numFlowDays= len(dates)
    simulatedFlow = np.zeros(numFlowDays)
    numSubB = 27
    flowSubB = 25 # 
    for i in range(numFlowDays):
        y = f_content[numSubB*i+flowSubB+8]
        # simulatedFlow[i] = y[38:49]
        simulatedFlow[i] = y[50:62]

    jdates= []
    for item in dates:
        date_time = item.strftime("%Y-%m-%d")
        jd = datestdtojd(date_time)
        jdates.append(jd)

    df = pd.DataFrame({'date':dates, 'year': dates.year, 'doy':jdates,'month':dates.month, 'day':dates.day, 'flow':simulatedFlow})
    return df

def mergeRegimes2(df, flowRegime):
    merged = pd.merge(df,flowRegime, left_on=['month','day'], right_on=['month','day'])
    merged = merged.sort_values(by="date")
    merged['SSE'] = (merged.flow_y - merged.flow_x)**2
    avg = merged.SSE.sum() / len(merged.SSE)
    merged['avg'] = avg
    return merged 

def calcFlows(filename,dates):
    ''' calculates flows for recession agriculture and environmental flows'''
    # read files
    f = open(filename,'r')
    f_content = f.readlines()
    f.close()
    
    # initialize numpy arrays
    numFlowDays= len(dates)
    simulatedFlow_RA = np.zeros(numFlowDays) 
    simulatedFlow_EF = np.zeros(numFlowDays)
    simulatedFlow_TR = np.zeros(numFlowDays)

    numSubB = 27
    flowSubB_RA = 24 # recession agriculture at sub 24
    flowSubB_EF = 25 # environmental flows at sub 25
    # flowSubB_TR = 27 # inflow to Turkana at sub 27 

    for i in range(numFlowDays):
        ra = f_content[numSubB*i+flowSubB_RA+8]
        ef = f_content[numSubB*i+flowSubB_EF+8]
        # tr = f_content[numSubB*i+flowSubB_TR+8]
        simulatedFlow_RA[i] = ra[50:62]
        simulatedFlow_EF[i] = ef[50:62]
        # simulatedFlow_TR[i] = tr[50:62]

    
    ra = pd.DataFrame({'date':dates,'year':dates.year,'month':dates.month, 'day':dates.day,'flow':simulatedFlow_RA})
    ef = pd.DataFrame({'date':dates,'year':dates.year,'month':dates.month, 'day':dates.day,'flow':simulatedFlow_EF})
    
    # vol = simulatedFlow_TR*86400
    # tr = pd.DataFrame({'date':dates,'year':dates.year,'month':dates.month, 'day':dates.day,'flow':simulatedFlow_TR,'vol':vol})
    return ra, ef

def mergeRegimes(df, targ):
    ''' merges recession targets with recession flows '''
    merged = pd.merge(df,targ, left_on=['month','day'], right_on=['month','day'])
    merged = merged.sort_values(by="date")
    return merged
        
def RecObj(df):
    ''' calculates flood recession objective:
    daily average squared positive difference between the flow in the lower omo and a target artificial flood, Aug 29 - Sep 15'''
    # fr = df.loc[df.targ > 0] # only look at days where there  is a flood recession target 
    fr = df[df['targ'] > 0]
    a = np.zeros(len(fr.flow))
    fr['zero'] = a
    fr['diff'] = fr.targ - fr.flow
    fr['obj'] = fr[['diff','zero']].apply(np.max,axis=1)
    fr['daily_obj'] = fr['obj']**2 
    recObj = fr.daily_obj.mean()
    return recObj


def EnvObj(df):
    df['SSE'] = (df.flow_y - df.flow_x)**2
    envObj = df.SSE.mean()
    return envObj