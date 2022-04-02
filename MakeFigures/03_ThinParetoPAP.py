# -*- coding: utf-8 -*-
"""
Created 6/21/2021

@author: Sarah Jordan

Make parallel axis plots comparing SWAT and DPS reservoir operating policies

Updated 9/18/2021 
- rename policies 
- transparency 
"""

# packages
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string


ref = pd.read_csv('../Optimization/ThinRef/thin_reference.ref', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
ref = ref.iloc[::-1]

# read in SWAT and DPS
swat = pd.read_csv('../Optimization/ThinRef/SWAT_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
dps = pd.read_csv('../Optimization/ThinRef/DPS_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
swat['source'] = 'SWAT'
dps['source'] = 'DPS'

swat_dps_all = pd.concat([swat, dps])

def PAP(ax, df,ex_df,title, lgd):


    table = df[['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton']]


    # Scale the data to minimum and maximum values 
    scaled = table.copy()
    for column in table.columns:
        if column != 'Source':
            mm = ex_df[column].min()
            mx = ex_df[column].max()
            scaled[column] = (table[column] - mm) / (mx - mm)
    
    # label is the soruce
    labs = df['source']

    # Plot all of the policies 
    d = 0
    s = 0
    for solution,l in zip(scaled.iterrows(),labs):
        if l == 'DPS':
            col = '#ff7f00'
            ls = "solid"
            d += 1 
            lbl = "Release Policy"
        elif l == 'SWAT':
            col = '#377eb8'
            ls = "solid"
            s +=1
            lbl = "Target Storage"
        else:
            col = 'lightgrey'
            ls = "solid"
            s +=1

        ys = solution[1]
        xs = range(len(ys - 1))

        ax.plot(xs, ys, c=col, linewidth = 2, label=lbl if (d == 1) or (s==1) else "", linestyle=ls, zorder =2.5 if (l=='DPS') else 0, alpha=0.3 if (l=='DPS') else 0.5)

    # Format the figure

    ax.annotate('', xy=(-0.14, 0.15), xycoords='axes fraction', xytext=(-0.14, 0.85),
        arrowprops=dict(arrowstyle="->", color='black'))

    ax.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax.set_xlim([0,np.shape(table)[1]-1])
    ax.set_ylim([0,1])

    ax.set_ylabel("Scaled Objective Values")
    # ax.set_xticks([0,1,2,3,4])
    ax.set_xticklabels(["Hydropower", "Environment", "Recession", "Sugar", "Cotton"])

    ax.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
    ax.tick_params(axis='x',which='both',top='off',bottom='off')

    
    # cbar.ax.set_xticklabels(['10','15','20','25','30'])
    # fig.axes[-1].set_xlabel('Scaled Environmental Flows Objective',fontsize=14)
    
    # make subplot frames invisible
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # draw in axes
    for i in np.arange(0,np.shape(table)[1],1):
        ax.plot([i,i],[0,1],c='k')

    # ax.set_title("Policy Source", size=18)
    ax.set_title(title)
    if lgd == True:
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)

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



# histogram
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

def plot_it(d, s, ax, lgd=False):
    bins = np.arange(0, 1.4, 0.1)
    ax.hist(d['dist'], bins, alpha=0.5, label="Release Policy", color='#ff7f00')
    ax.hist(s['dist'], bins, alpha=0.5, label="Target Storage", color='#377eb8')
    if lgd==True:
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
    # ax.xaxis.set_ticklabels([])
    ax.set_xlabel("Distance from Ideal Policy")
    ax.set_ylabel("Number of Policies")

    ax.xaxis.set_ticks(bins)

dps_distances = calc_dist(dps, swat_dps_all)
swat_distances = calc_dist(swat, swat_dps_all)

dps_distances_comb = calc_dist(ref[ref.source =='DPS'], swat_dps_all)
swat_distances_comb = calc_dist(ref[ref.source == 'SWAT'], swat_dps_all)


# print("SWAT:", len(ref[ref['source'] == 'SWAT']))
# print("DPS:", len(ref[ref['source'] == 'DPS']))

sns.set(style="white")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.set_size_inches([6.3625*2, 6.3625])



PAP(ax1, swat_dps_all, swat_dps_all, "", False)
plot_it(dps_distances, swat_distances, ax2)

PAP(ax3, ref, swat_dps_all, "", True)
plot_it(dps_distances_comb, swat_distances_comb, ax4,lgd=True)


ax_ls = [ax1, ax2, ax3, ax4]
for n in range(len(ax_ls)):
    ax_ls[n].text(0.01, 0.9, "("+ string.ascii_lowercase[n] + ")", transform=ax_ls[n].transAxes, 
            size=13, weight='bold')


fig.tight_layout()
fig.savefig(os.path.join('./Figures/', "03_HistoricalParallelAxisPlot_4sub.svg"))
fig.savefig(os.path.join('./Figures/', "03_HistoricalParallelAxisPlot_4sub.png"))
plt.clf()