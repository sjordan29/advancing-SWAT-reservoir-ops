'''
Calculate flow timeseries for each policy and each climate projection. 
'''

from Flows import * 
import pandas as pd 
from mpi4py import MPI
import os 
import sys
import numpy as np

# Climate Scenarios 
fut_dates = pd.date_range(start="2019-01-01",end="2099-12-31", freq='d')


def FlowCSV(fpath, file, rank):
    if len(str(rank)) < 2:
        rank = "0" + str(rank)
    flows = calcEnvFlow(os.path.join(fpath, file,'TxtInOut_%s/SWATfiles/output.rch') % rank, fut_dates)
    flows.to_csv('/scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/Timeseries/SWAT/%s_%s_Flow.csv' % (file, rank))

# Parallel
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# fpath = '/sfs/lustre/bahamut/scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/DPS/'
# fpath = '/sfs/lustre/bahamut/scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/Uncontrolled/'
fpath = '/sfs/lustre/bahamut/scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/SWAT/'
# files = os.listdir(fpath)
# file = files[rank]

for file in os.listdir(fpath):
    if file == "SWATfiles":
        print("skipping", file)
        pass
    elif file == "Objectives":
        print("skipping", file)
        pass
    elif ".reference" in file:
        print("skipping", file)
        pass
    elif file == "HadGEM2-ES.rcp45":
        print("skipping", file)
        pass
    elif file == "CCSM4.rcp26":
        print("skipping", file)
        pass
    elif file == "GFDL-CM3.rcp45":
        print("skipping", file)
        pass 
    else:
        print("Starting", file)
        FlowCSV(fpath, file, rank)