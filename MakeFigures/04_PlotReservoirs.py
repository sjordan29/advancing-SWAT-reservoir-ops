
# packages
import pandas as pd
import os 
import numpy as np
import matplotlib.pyplot as plt 
import datetime as dt
from matplotlib.pyplot import cm
import datetime
import seaborn as sns
from Hydropower import *
import string

def hydroPlots(TxtFold_dps, TxtFold_swat, dates, title):
    Objectives = ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'] 
    colors = ['#999999', "forestgreen", "cornflowerblue", "mediumpurple", "orange"]
    folders = ['TxtInOut_0', 'TxtInOut_1', 'TxtInOut_2','TxtInOut_3','TxtInOut_4']

    sns.set(style='darkgrid')
    # sns.set_context('poster')

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    # fig.set_size_inches([16,8])
    # fig.rcParams.update({'font.size': 22})

    for obj,c,fold in zip(Objectives,colors,folders):
        dps, dps_dam, dps_head, dps_stor = calcHydropower( TxtFold_dps + fold + '/SWATfiles/output.rsv', dates)
        swat, swat_dam, swat_head, swat_stor = calcHydropower(TxtFold_swat + fold + '/SWATfiles/output.rsv', dates)
        dps_mean = dps_stor.groupby('day').mean()
        swat_mean = swat_stor.groupby('day').mean()

        mx_g =1470000.0* 10**4
        mx_k = 570000.0* 10**4    
         
        mn_g = 292120.0* 10**4
        mn_k = 76000.0* 10**4

        swat_giii = (swat_mean.GibeIII - mn_g) / (mx_g - mn_g) * 100
        dps_giii = (dps_mean.GibeIII - mn_g) / (mx_g - mn_g) * 100
        swat_k = (swat_mean.Koysha - mn_k) / (mx_k - mn_k) * 100
        dps_k = (dps_mean.Koysha - mn_k) / (mx_k - mn_k) * 100
    
        ax1.plot(swat_mean.index, swat_giii, label=obj,color=c, linestyle='dashed')
        ax2.plot(dps_mean.index, dps_giii, label=obj, color=c)
        ax3.plot(swat_mean.index, swat_k, label=obj,color=c, linestyle='dashed')
        ax4.plot(dps_mean.index, dps_k, label=obj, color=c)

    # outside labels
    for ax, i in zip([ax1, ax2, ax3, ax4], range(4)):
        ax.set_xticks([60,152,244,335])
        ax.set_xticklabels(['Mar','Jun','Sep','Dec'],fontsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.text(0.005, 0.9, "("+ string.ascii_lowercase[i+1] + ")", transform=ax.transAxes, 
            size=13, weight='bold')
    for ax in [ax1, ax3]:
        ax.set_ylabel("Storage (%)", fontsize=12)
    for ax in [ax3, ax4]:
        ax.set_xlabel("Day of Year", fontsize=12)
    for ax in [ax1, ax2]:
        ax.set_ylim(-5,105)
    for ax in [ax3, ax4]:
        ax.set_ylim(-5,105)
    ax1.set_title("Target Storage:\nGibe III Average Storage", fontsize=12)
    ax2.set_title("Release Policies:\nGibe III Average Storage", fontsize=12)
    ax3.set_title("Target Storage:\nKoysha Average Storage", fontsize=12)        
    ax4.set_title("Release Policies:\nKoysha Average Storage", fontsize=12)

    handles, labels = fig.axes[-1].get_legend_handles_labels()
    lgd = fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.55,-.08),title = "Best Policy For:", ncol=3, fontsize=10, title_fontsize="small")
    text = ax.text(-0.2,1.05, "", transform=ax.transAxes)
    fig.tight_layout(h_pad=0.2)

    fig.set_size_inches([6.3625, 6.3625])
    plt.savefig('Figures/' + title, bbox_inches='tight')
    plt.clf()

hydroPlots("../../BestPolicyEachObj/DPS/", "../../BestPolicyEachObj/SWAT/", pd.date_range(start="1989-01-01",end="2018-12-31", freq='d'), "04_ReservoirLevels.svg")
hydroPlots("../../BestPolicyEachObj/DPS/", "../../BestPolicyEachObj/SWAT/", pd.date_range(start="1989-01-01",end="2018-12-31", freq='d'), "04_ReservoirLevels.png")