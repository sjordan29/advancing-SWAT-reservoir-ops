from glob import glob 
import pandas as pd
import os
import numpy as np

fpath_dps = '../Timeseries/DPS'
projections = np.unique([f.split("_")[0] for f in os.listdir(fpath_dps)])
Koysha = dict.fromkeys(projections)
GIII = dict.fromkeys(projections)
GI = dict.fromkeys(projections)


def allowDictionary(proj, k_dict, gi_dict, giii_dict, loc):
    # files = [f for f in sorted(glob('../Timeseries/%s/%s*_ResHead.csv' % (loc,proj)))  ]
    files = [f for f in sorted(glob('../Timeseries/%s/%s*_ResInflow.csv' % (loc,proj)))  ]
    k_df = pd.DataFrame()
    gi_df = pd.DataFrame()
    giii_df = pd.DataFrame()


    for f in files:
        df = pd.read_csv(f, parse_dates=True, index_col='date')
        k_df["P" + f.split("_")[1]] = df['Koysha']
        gi_df["P" + f.split("_")[1]] = df['GibeI']
        giii_df["P" + f.split("_")[1]] = df['GibeIII']



    k_df.index = pd.to_datetime(df.index)
    gi_df.index = pd.to_datetime(df.index)
    giii_df.index = pd.to_datetime(df.index)

    k_dict[proj] = k_df
    gi_dict[proj] = gi_df
    giii_dict[proj] = giii_df

    return k_dict, gi_dict, giii_dict


for proj in projections:
    print("Starting %s" % proj)

    Koysha, GI, GIII = allowDictionary(proj, Koysha, GI, GIII, "DPS")



for proj in projections:
    Koysha[proj].to_csv('../Timeseries/DPS/%s_KoyshaFlowIn.csv' % proj)
    GI[proj].to_csv('../Timeseries/DPS/%s_GIFlowIn.csv' % proj)
    GIII[proj].to_csv('../Timeseries/DPS/%s_GIIIFlowIn.csv' % proj)