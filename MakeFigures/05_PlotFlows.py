import pandas as pd
import os 
import numpy as np
import matplotlib.pyplot as plt 
import datetime as dt
from matplotlib.pyplot import cm
import datetime
from Flows import *
import seaborn as sns
import string


def envRecPlots(TxtFold_dps, TxtFold_swat, dates, title):
    Objectives = ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'] 
    colors = ['#999999', "forestgreen", "cornflowerblue", "mediumpurple", "orange"]
    folders = ['TxtInOut_0', 'TxtInOut_1', 'TxtInOut_2','TxtInOut_3','TxtInOut_4']

    sns.set(style='darkgrid')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

    for obj,c,fold in zip(Objectives,colors, folders):
        dps_rec = calcFloodRecession(TxtFold_dps + fold + '/SWATfiles/output.rch', dates)
        swat_rec = calcFloodRecession(TxtFold_swat + fold +'/SWATfiles/output.rch', dates)

        fr = pd.read_csv('RA_Targs.csv',header=None)
        fr.columns = ['date','targ']
        dates2 = pd.date_range(start="1989-01-01",end="1989-12-31", freq='d')
        jdates2 = []
        for item in dates2:
            date_time = item.strftime("%Y-%m-%d")
            jd = datestdtojd(date_time)
            jdates2.append(jd)
        recessionAg = pd.DataFrame({'month': dates2.month, 'day': dates2.day, 'targ':fr['targ']})
        fr['doy'] = jdates2

        def mergeRegimes(df):
            merged = pd.merge(df,recessionAg, left_on=['month','day'], right_on=['month','day'])
            merged = merged.sort_values(by="date")
            return merged 

        dps_rec = mergeRegimes(dps_rec)
        swat_rec = mergeRegimes(swat_rec)


        # Environmental Flows: daily average squared distance between # the flow in the omo river delta and the natural pattern
        dps_env= calcEnvFlow(TxtFold_dps + fold + '/SWATfiles/output.rch', dates)
        swat_env= calcEnvFlow(TxtFold_swat + fold + '/SWATfiles/output.rch', dates)

        freg = pd.read_csv('omorateRegime.txt', sep='\t',header=None)
        flowRegime = pd.DataFrame({'month': dates2.month, 'day': dates2.day, 'flow':freg.values[0]})
        flowRegime_plot = pd.DataFrame({'doy':jdates2, 'flow':freg.values[0]})

        dps_env = mergeRegimes2(dps_env, flowRegime)
        swat_env = mergeRegimes2(swat_env, flowRegime)
        
        
        # plot 
        
        dps_mean_rec = dps_rec.groupby('doy').mean()
        swat_mean_rec = swat_rec.groupby('doy').mean()
        dps_mean_env = dps_env.groupby('doy').mean()
        swat_mean_env = swat_env.groupby('doy').mean()

        ax1.plot(swat_mean_rec.index, swat_mean_rec.flow, label=obj,color=c, linestyle = 'dashed')        
        ax2.plot(dps_mean_rec.index, dps_mean_rec.flow, label=obj, color=c)
        ax3.plot(swat_mean_env.index, swat_mean_env.flow_x, label=obj,color=c, linestyle = 'dashed')
        ax4.plot(dps_mean_env.index, dps_mean_env.flow_x, label=obj,color=c)

        
        ax_ys = [ax1, ax3]
        ax_xs = [ax3, ax4]
        for ax in ax_ys:
            ax.set_ylabel("Flow (cms)", fontsize = 12)
        for ax in ax_xs:
            ax.set_xlabel("Day of Year", fontsize = 12)

        for ax,i in zip([ax1, ax2, ax3, ax4], range(4)):
            ax.set_xticks([60,152,244,335])
            ax.set_xticklabels(['Mar','Jun','Sep','Dec'],fontsize=12)
            ax.tick_params(axis='y', labelsize=12)
            ax.set_ylim(0,2000)
            ax.text(0.005, 0.9, "("+ string.ascii_lowercase[i] + ")", transform=ax.transAxes, 
                size=13, weight='bold')
        
        
            
        ax1.set_title("Target Storage:\nFlood Recession", size=12)
        ax2.set_title("Release Policies:\nFlood Recession", size=12)

        ax3.set_title("Target Storage:\nEnvironmental Flows", size=12)
        ax4.set_title("Release Policies:\nEnvironmental Flows", size = 12)
        
    ax1.plot(fr.doy, fr.targ,label="Target",color='red',linestyle="dotted",linewidth=3)
    ax2.plot(fr.doy, fr.targ,label="Target",color='red',linestyle="dotted",linewidth=3)
    ax3.plot(flowRegime_plot.doy, flowRegime_plot.flow,label="Target",color='red',linestyle="dotted",linewidth=3)
    ax4.plot(flowRegime_plot.doy, flowRegime_plot.flow,label="Target",color='red',linestyle="dotted",linewidth=3)

    handles, labels = fig.axes[-1].get_legend_handles_labels()
    lgd = fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.55,-.08),title = "Best Policy For:", ncol=3, fontsize=10, title_fontsize="small")
    text = ax.text(-0.2,1.05, "", transform=ax.transAxes)
    fig.tight_layout(h_pad=0.2)

    fig.set_size_inches([6.3625, 6.3625])
    plt.savefig('Figures/' + title, bbox_extra_artists=(lgd,text), bbox_inches='tight')
    plt.clf()


envRecPlots("../../BestPolicyEachObj/DPS/", "../../BestPolicyEachObj/SWAT/", pd.date_range(start="1989-01-01",end="2018-12-31", freq='d'), "05_DownstreamFlows.svg")
envRecPlots("../../BestPolicyEachObj/DPS/", "../../BestPolicyEachObj/SWAT/", pd.date_range(start="1989-01-01",end="2018-12-31", freq='d'), "05_DownstreamFlows.png")