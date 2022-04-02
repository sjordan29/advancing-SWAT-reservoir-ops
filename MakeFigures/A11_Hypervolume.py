# -*- coding: utf-8 -*-
"""
Created 6/21/2021

@author: Sarah Jordan

Compare Hypervolume vs step for DPS vs SWAT reservoir optimization
"""

import pandas as pd
import glob
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('metrics/')
DPS_files = glob.glob('DPS*.metrics')
SWAT_files = glob.glob('SWAT*.metrics')

DPS_data = []
for csv in DPS_files:
    frame = pd.read_csv(csv, sep = ' ')
    frame['step'] = int(os.path.basename(csv)[-10:-8].replace("p", ""))
    DPS_data.append(frame)


SWAT_data = []
for csv in SWAT_files:
    frame = pd.read_csv(csv, sep = ' ')
    frame['step'] = int(os.path.basename(csv)[-10:-8].replace("p", ""))
    SWAT_data.append(frame)


DPS_df = pd.concat(DPS_data, ignore_index=True)
SWAT_df = pd.concat(SWAT_data, ignore_index=True)

DPS_df = DPS_df.sort_values(by=['step'])
SWAT_df = SWAT_df.sort_values(by=['step'])

DPS_df['step'] = DPS_df['step'] * 2
SWAT_df['step'] = SWAT_df['step'] * 2

# print(DPS_combined.columns)
sns.set()
fig, (ax1) = plt.subplots(1,1)
ax1.plot(SWAT_df["step"], SWAT_df['#Hypervolume'], label="Target Storage", color='#377eb8', linestyle='solid')
ax1.plot(DPS_df['step'], DPS_df['#Hypervolume'], label="Release Policy", color='#ff7f00', linestyle='solid')

ax1.set_ylabel("Hypervolume")
for ax in [ax1]:
    ax.set_xlabel("1000 NFE")
    ax.set_ylim(0, 1)
plt.legend(bbox_to_anchor=(1.03,-.17), ncol=2)
fig.set_size_inches([3.8625, 3.8625])


plt.savefig('../Figures/A11_Hypervolume.svg', bbox_inches='tight')