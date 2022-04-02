# packages
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string
from matplotlib import patheffects as pe

# filepaths
dps = pd.read_csv('ThinRef/DPS_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
swat = pd.read_csv('ThinRef/SWAT_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])


# plotting function
def PAP(ax, df,ex_df,title, lgd, h_dps, h_swat):


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
            ls = 'solid'
            lbl = ""

        ys = solution[1]
        xs = range(len(ys - 1))
        if l == "DPS":
            if int(solution[0]) in h_dps:
                ax.plot(xs, ys, c=col, linewidth = 2,  zorder =3.5, \
                         path_effects=[pe.Stroke(linewidth=5, foreground='k'), pe.Normal()])
        elif l == "SWAT":
            if int(solution[0]) in h_swat:
                ax.plot(xs, ys, c=col, linewidth = 2,  zorder =3.5, \
                         path_effects=[pe.Stroke(linewidth=5, foreground='k'), pe.Normal()])
            
        ax.plot(xs, ys, c=col, linewidth = 2, label=lbl if (d == 1) or (s==1) else "", linestyle=ls, zorder =2.5 if (l=='SWAT') else 1)

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
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)


# robust indices
dps_r = dps.iloc[[0, 3, 5, 7, 13, 15, 31, 34, 35, 43, 44, 51, 67, 69, 70, 71, 77, 89, 90, 95],:]
swat_r = swat.iloc[[1, 11, 21]]

swat_r = swat_r.reset_index()
dps_r = dps_r.reset_index()
swat_r['source'] = 'SWAT'
dps_r['source'] = 'DPS'
combo_r = pd.concat([dps_r, swat_r])

# all data 
swat_dps_all = pd.concat([swat, dps])
swat_dps_all['source'] = 'Skip'


# set up figure
sns.set(style="white")
fig, ax  = plt.subplots(1,1)
fig.set_size_inches([6.3625, 3.3625])

PAP(ax, swat_dps_all, swat_dps_all, "", False, None, None)
PAP(ax, combo_r, swat_dps_all, "", True,[8], [1])

# ax_ls = [ax1, ax2]
# for n in range(len(ax_ls)):
#     ax_ls[n].text(0.01, 0.9, "("+ string.ascii_lowercase[n] + ")", transform=ax_ls[n].transAxes, 
#             size=13, weight='bold')

ax.text(0.008, 0.95, "(a)", transform=ax.transAxes, 
        size=13, weight='bold')
fig.tight_layout()
fig.savefig(os.path.join('./Figures', "07_PAP_SelectedPols_ReservoirCC.svg"))

plt.clf()