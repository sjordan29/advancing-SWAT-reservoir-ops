# -*- coding: utf-8 -*-
"""
Created 11/20/2021

@author: Sarah Jordan

Make histogram of distance from ideal point. 
"""

# packages
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string

# read in combined Pareto set
ref = pd.read_csv('ThinRef/thin_reference.ref', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
ref = ref.iloc[::-1]

# read in SWAT and DPS
swat = pd.read_csv('ThinRef/SWAT_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
dps = pd.read_csv('ThinRef/DPS_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
swat['source'] = 'SWAT'
dps['source'] = 'DPS'
swat_dps_all = pd.concat([swat, dps])

# find sources of combined Pareto Set 
source = []
for index, row in ref.iterrows():
    check_swat = swat.loc[(round(swat['Hydropower'],5) == round(row['Hydropower'],5)) & (round(swat['Environment'],5) == round(row['Environment'],5)) & (round(swat['Recession'],5) == round(row['Recession'], 5)) & (round(swat['Sugar'],5) == round(row['Sugar'],5)) & (round(swat['Cotton'],5) == round(row['Cotton'],5))]
    check_dps = dps.loc[(round(dps['Hydropower'],5) == round(row['Hydropower'],5)) & (round(dps['Environment'],5) == round(row['Environment'],5)) & 
                             (round(dps['Recession'],5) == round(row['Recession'], 5)) &
                             (round(dps['Sugar'],5) == round(row['Sugar'],5)) & (round(dps['Cotton'],5) == round(row['Cotton'],5))]
    if len(check_swat['Hydropower']) > 0:
        val = 'SWAT'
    elif len(check_dps['Hydropower']) > 0:
        val = 'DPS'
    else:
        val = 'Error'
    source.append(val)

ref['source'] = source


# ideal point
def calc_dist(df, ex_df):
    table = df[['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton']]
    scaled = table.copy()
    for column in table.columns:
        if column != 'Source':
            mm = ex_df[column].min()
            mx = ex_df[column].max()
            scaled[column] = (table[column] - mm) / (mx - mm)

    scaled['dist'] = np.sqrt(scaled['Hydropower'] ** 2 + scaled['Environment'] ** 2 + scaled['Recession'] ** 2 + scaled['Sugar'] ** 2 + scaled['Cotton'] ** 2)
    return scaled



def plot_it(d, s, suffix=""):
    fig, ax = plt.subplots()
    fig.set_size_inches([6.3625, 6.3625])
    sns.set(style="white")
    bins = np.arange(0, 1.4, 0.1)
    ax.hist(d['dist'], bins, alpha=0.5, label="Release Policy", color='#ff7f00')
    ax.hist(s['dist'], bins, alpha=0.5, label="Target Storage", color='#377eb8')
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.125), ncol=2)
    ax.xaxis.set_ticklabels([])
    ax.set_xlabel("Distance from Ideal Policy")
    ax.set_ylabel("Number of Policies")
    ax.xaxis.set_ticks(bins)

    fig.tight_layout()
    fig.savefig(os.path.join('./Figures/', "09_Tradeoffs%s.svg" % suffix))
    plt.clf()

dps_distances = calc_dist(dps, swat_dps_all)
swat_distances = calc_dist(swat, swat_dps_all)

plot_it(dps_distances, swat_distances)

dps_distances_comb = calc_dist(ref[ref.source =='DPS'], swat_dps_all)
swat_distances_comb = calc_dist(ref[ref.source == 'SWAT'], swat_dps_all)

plot_it(dps_distances_comb, swat_distances_comb, "_combined")
