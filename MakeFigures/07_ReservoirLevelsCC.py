'''
Plot reservoir levels under CC
'''

import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import os
import pandas as pd
from matplotlib import colors
from matplotlib import cm as cmx
from Hydropower import *
import string
import seaborn as sns
from utils import * 

# filepaths
fpath_ts = '../Timeseries/Uncontrolled'
fpath_d = '../Extremes/DPS'

# define projections and sort
projections = np.unique([f.split("_")[0] for f in os.listdir(fpath_d) if 'csv' in f])
sorted_projs = DryWet(projections,fpath_ts)

# define color dictionary - for coloring projections 
# red to blue = dry to wet
col_dict = {}
for proj,i in zip(sorted_projs, range(len(projections))):
    col_dict[proj] = i/47


# P35 is compromise dps solution
# P11 is compromise swat solution
# read data in
a,b,c, dps_h = calcHydropower('../../Historical/DPS/TxtInOut_35/SWATfiles/output.rsv', pd.date_range(start="1989-01-01",end="2018-12-31", freq='d'))
a,b,c, swat_h = calcHydropower('../../Historical/SWAT/TxtInOut_11/SWATfiles/output.rsv', pd.date_range(start="1989-01-01",end="2018-12-31", freq='d'))

# calculate mean daily values
dps_mean =dps_h.groupby('day').mean()
swat_mean = swat_h.groupby('day').mean()



fig,((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
sns.set(style="dark")

# axis_dict = {'P14': [ax1, ax2], 'P41': [ax3, ax4], 'P07':[ax5, ax6], 'P92':[ax7,ax8]}
dates = pd.date_range(start="2019-01-01",end="2099-12-31", freq='d')
cbar = plt.cm.get_cmap('RdBu')
titles = {'P11':'Target Storage', 'P35':'Release Policy', 'P07':'AMS/ENV', 'P41': '7QS/AMS'}
mn_g = 292120 * 10**4
mx_g = 1470000 * 10**4
mn_k = 76000 * 10**4
mx_k = 570000 * 10**4

def hydroPlots(policy, proj, ax_g, ax_k, col_dict, name):
    df = pd.read_csv('../ReservoirTS/Chapter1/%s_%s_%s_Storage.csv' %(name, policy, proj))
    dps_mean = df.groupby('day').mean()
    g_vals = (dps_mean.GibeIII - mn_g) / (mx_g - mn_g) * 100
    ax_g.plot(dps_mean.index, g_vals, color=cbar(col_dict[proj]))
    ax_g.set_ylim(-5,105)
    ax_g.set_title(titles[policy], fontsize=14)
    ax_g.tick_params(axis='y', labelsize=14)
    k_vals = (dps_mean.Koysha - mn_k) / (mx_k - mn_k) * 100
    ax_k.plot(dps_mean.index, k_vals, color=cbar(col_dict[proj]))
    ax_k.set_ylim(-5, 105)
    ax_k.set_title(titles[policy], fontsize=14)
    ax_g.set_xticklabels("")
    ax_k.set_xticklabels("")
    ax_k.set_yticklabels("")
    ax_g.set_ylabel("Storage (%)", fontsize=14)


for proj in projections:
    hydroPlots("P35", proj, ax1,ax2, col_dict, "DPS")
    hydroPlots("P11", proj, ax3, ax4, col_dict, "SWAT")

for ax in [ax3, ax4]:
    ax.set_xticks([45,137,229,319])
    ax.set_xticklabels(['Mar','Jun','Sep','Dec'],fontsize=14)

    
sm = plt.cm.ScalarMappable(cmap='RdBu')
sm.set_array([0,1])
cbar_ax = fig.add_axes([0.25, -0.02, 0.6, 0.03])
cbar = fig.colorbar(sm, ax=ax, cax = cbar_ax, orientation='horizontal', ticks=np.arange(0.0,2,1))
cbar.ax.set_xticklabels(['Dry', 'Wet'],fontsize=14)

ax_ls = [ax1, ax2, ax3, ax4]
for i in range(len(ax_ls)):
     ax_ls[i].text(0.008, 1.02, "("+ string.ascii_lowercase[i+1] + ")", transform=ax_ls[i].transAxes, 
        size=13, weight='bold')
                
ax1.plot(dps_mean.index, (dps_mean.GibeIII - mn_g) / (mx_g - mn_g) * 100, zorder=5, linewidth=5, color="k")
ax2.plot(dps_mean.index, (dps_mean.Koysha- mn_k) / (mx_k - mn_k) * 100, zorder=5, linewidth=5, color="k")
ax3.plot(swat_mean.index, (swat_mean.GibeIII - mn_g) / (mx_g - mn_g) * 100, zorder=5, linewidth=5, color="k")
ax4.plot(swat_mean.index, (swat_mean.Koysha - mn_k) / (mx_k - mn_k) * 100, zorder=5, linewidth=5, color="k")

        
fig.text(0.345, 1.0, 'Gibe III', ha='center', fontsize=18)
fig.text(0.77, 1.0, 'Koysha', ha='center', fontsize=18)


fig.set_size_inches([6.325,6.325])
fig.tight_layout()
plt.savefig('Figures/07_ReservoirLevelsCC.svg', bbox_inches='tight')