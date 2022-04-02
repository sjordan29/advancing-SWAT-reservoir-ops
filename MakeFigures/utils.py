import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# functions 
def IndexName(f):
    name_elems = f.split("_")
    i_name = name_elems[0]
    return i_name

def InitializeDicts(mc_dict, lc_dict, flist, col_names):
    for key in mc_dict:
        mc_dict[key] = pd.DataFrame(np.nan,index=flist, columns=col_names)
        lc_dict[key] = pd.DataFrame(np.nan,index=flist, columns=col_names)
    return mc_dict, lc_dict

def ParseObjectives(fpath, f, Objectives, mc_dict, lc_dict):
    # get index name
    i_name = IndexName(f)

    # column name
    col = "P" + f.split("_")[1]

    df = pd.read_csv(os.path.join(fpath, f), names=['mc', 'lc'])
    
    for i in range(5):
        obj = Objectives[i]
        mc_dict[obj].at[i_name,col] = df['mc'][i]
        lc_dict[obj].at[i_name,col] = df['lc'][i]
    return mc_dict, lc_dict
    
    
def combineData(fpath, mc_dict, lc_dict, npol):
    '''
    fpath = filepath of obj files
    mc_dict / lc_dict = mid-century or late century dictionary
    '''
    
    files = os.listdir(fpath)
    
    # intitalize empty dfs 
    # get all index names
    flist = []
    for file in files:
        i_name = IndexName(file)
        flist.append(i_name)
    flist.sort()
    flist = np.unique(flist)
    
    # columns
    col_names = []
    for i in range(npol):
        if len(str(i)) < 2:
            c = "P0" + str(i)
        else:
            c = "P" + str(i)
        col_names.append(c)
        
    # set up dictionaries 
    mc_dict, lc_dict = InitializeDicts(mc_dict, lc_dict, flist, col_names)
    
    # parse
    for file in files:
        mc_dict, lc_dict = ParseObjectives(fpath, file, Objectives, mc_dict, lc_dict) 
    return mc_dict, lc_dict 


# def printDict(dict_name):
#     dict1 = {x: dict_name[x] for x in dict_name if x not in ['Year']}
#     sorted_dict = {}
#     sorted_keys = sorted(dict1, key=dict1.get, reverse=False)  # [1, 3, 2]

#     for w in sorted_keys:
#         sorted_dict[w] = dict1[w]
        
#     keys = [f for f in sorted_dict.keys()]

#     return keys





def findMinMax(table):
    mn = 1000000000000000000
    mx = -10000000000000000
    for column in table.columns:
        if table[column].min() < mn:
            mn = table[column].min()
        if table[column].max() > mx:
            mx = table[column].max()
    return mn, mx 

def ScaleTables(table, mn, mx):
    scaled = table.copy()
    for column in table.columns:
        scaled[column] = (table[column] - mn) / (mx - mn)
    return scaled
        
def PlotIt(table, color, linestyle, label, ax):
    xs = range(len(table.iloc[:, 0]))
    for col in table.columns:
        ax.plot(xs, table[col], c=color, linewidth = 2, label=label if (d==1) or (s==1) or (u==1) else "", linestyle=linestyle, alpha=0.7)
        d+=1 
        s+=1
        u+=1
    

def PAP(ax, dps_dict, swat_dict, uc_dict, obj):
    dps_table = dps_dict[obj]
    swat_table = swat_dict[obj]
    uc_table = uc_dict [obj]
    
    dps_mn, dps_mx = findMinMax(dps_table)
    swat_mn, swat_mx = findMinMax(swat_table)
    uc_mn, uc_mx = findMinMax(uc_table)
    
    mn = min([dps_mn, swat_mn, uc_mn])
    mx = max([dps_mx, swat_mx, uc_mx])
    
    dps_scaled = ScaleTables(dps_table, mn, mx)
    swat_scaled = ScaleTables(swat_table, mn, mx)
    uc_scaled = ScaleTables(uc_table, mn, mx)

    PlotIt(swat_scaled, '#377eb8', 'solid', 'SWAT', ax)        
    PlotIt(dps_scaled, '#ff7f00', 'dotted', 'DPS', ax)
    PlotIt(uc_scaled, 'black', 'dashed', 'uncontrolled', ax)

    ax.set_title(obj)
    ax.set_ylabel("Objective Value")


def intersection(lst1, lst2, lst3, lst4, lst5): 
    a = [item for item in lst1 if item in lst2]
    b = [item for item in lst3 if item in a]
    c = [item for item in lst4 if item in b]
    d = [item for item in lst5 if item in c]
    return d

def FindCommonElements(scenario_dict, uc, Objectives):
    ND = dict.fromkeys(Objectives)
    for key in ND:
        ND[key] = {}
        for col in scenario_dict[key].columns:
            ND[key][col] = []

    for key in scenario_dict:
        for col in scenario_dict[key].columns:
            for val_dps, val_uc,i in zip(scenario_dict[key][col], uc[key]['PUC'], scenario_dict[key].index):
                if val_dps < val_uc:
                    ND[key][col].append(i) 
                    
    
    pols = []
    for col in ND['Hydropower']:
        ls = intersection(ND['Hydropower'][col], ND['Environment'][col],ND['Recession'][col],ND['Sugar'][col],ND['Cotton'][col])
        if len(ls) == 48:
            pols.append(col)
            
    return pols  
                
def PlotIt(x_ls, table, color, linestyle, label, ax,d,s,u):
    # xs = range(len(table.iloc[:, 0]))
    xs = x_ls
    for col in table.columns:
        ax.plot(xs, table[col], c=color, linewidth = 2, label=label if (d==1) or (s==1) or (u==1) else "",
                linestyle=linestyle, zorder = 2 if label == "Target Storage" else 1, alpha=0.4 if (label=='Target Storage') else 0.6)
        d+=1 
        s+=1
        u+=1



def PAP_ltd(ax, dps_dict, swat_dict, uc_dict, obj,dps_cols, swat_cols, dps_addl, swat_addl, uc_addl, x_ls, uc_huc = None, huc_blw=None):
    dps_table = dps_dict[obj]
    swat_table = swat_dict[obj]
    uc_table = uc_dict[obj]
    
    # print(dps_dict)
    # print("----")
    
    dps_mn, dps_mx = findMinMax(dps_dict[obj])
    swat_mn, swat_mx = findMinMax(swat_dict[obj])
    uc_mn, uc_mx = findMinMax(uc_dict[obj])
    
    dps_mn_addl, dps_mx_addl = findMinMax(dps_addl[obj])
    swat_mn_addl, swat_mx_addl = findMinMax(swat_addl[obj])
    uc_mn_addl, uc_mx_addl = findMinMax(uc_addl[obj])
    
    mn = min([dps_mn, swat_mn, uc_mn, dps_mn_addl, swat_mn_addl, uc_mn_addl])
    mx = max([dps_mx, swat_mx, uc_mx, dps_mx_addl, swat_mx_addl, uc_mx_addl])
    
    dps_scaled = ScaleTables(dps_table, mn, mx)
    swat_scaled = ScaleTables(swat_table, mn, mx)
    uc_scaled = ScaleTables(uc_table, mn, mx)
    
    # print(dps_scaled)
    
    d=2
    s=2
    u=2
    PlotIt(x_ls, swat_scaled, 'lightgrey', 'solid', None, ax,d,s,u)
    PlotIt(x_ls, dps_scaled, 'lightgrey', 'solid', None, ax,d,s,u)
    s=1
    PlotIt(x_ls, swat_scaled[swat_cols], '#377eb8', 'solid', 'Target Storage', ax, d,s,u) 
    d=1
    PlotIt(x_ls, dps_scaled[dps_cols], '#ff7f00', 'solid', 'Release Policy', ax, d, s, u)
    u=1
    PlotIt(x_ls, uc_scaled, 'black', 'dashed', 'Uncontrolled', ax, d, s, u)
    
    if huc_blw != None:
        i_start = None
        n = 0 
        for i in dps_dict['Hydropower'].index:
            if i == huc_blw:
                i_start = n
            n+=1
        ax.axvline(uc_huc, alpha = 0.8, color = 'red', zorder = 100, linestyle = 'dashed', label = 'Historical Flow')
        
    else:
        ax.axvline(0, alpha = 0.8, color = 'red', zorder = 100, linestyle = 'dashed', label = 'Historical Flow')

        # ax.axvspan(i_start, i_start + 1, alpha=0.5, color='red',zorder=100, label="Historical Flow")

    # ax.set_xticks(np.arange(0,48,1))
    # ax.set_xticks([0,47])
    # ax.set_xlim([0,47])
    ax.set_xticks([min(x_ls), max(x_ls)])
    ax.set_xlim([min(x_ls), max(x_ls)])
    ax.set_ylim([0,1])
    # ax.set_xticklabels(xlabels,fontsize=14)
    ax.tick_params(axis='y',which='minor',reset=True,labelleft='off',left='off',right='off')
    # ax.tick_params(axis='x',which='major',top='off',bottom='off')
    
    t = obj
    if obj == "Environment": 
        t = obj + "al Flows"
    elif obj == "Recession":
        t = obj + " Agriculture"
    elif obj in ['Cotton', 'Sugar']:
        t = obj + " Yield"

    ax.set_title(t)
#     ax.set_ylabel("Objective Value", fontsize=16)
#     ax.set_xticklabels("")
#     if obj == "Cotton":
#         ax.set_xlabel("Climate Projections", fontsize=16)




def printDict(dict_name):
    '''
    sorts keys by their values  
    '''
    dict1 = {x: dict_name[x] for x in dict_name if x not in ['Year']}
    sorted_dict = {}
    sorted_keys = sorted(dict1, key=dict1.get, reverse=False)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = dict1[w]
        
    keys = [f for f in sorted_dict.keys()]

    return keys


def DryWet(projections, fpath_ts):
    '''
    sorts projections from wet to dry 
    '''
    UC_ts = dict.fromkeys(projections)
    for proj in projections:
        UC_ts[proj] = pd.read_csv(os.path.join(fpath_ts, '%s_UC_Flow.csv' % proj), index_col = 'Unnamed: 0')
    
    UC_mean = dict.fromkeys(projections)
    for proj in projections:
        UC_mean[proj] = UC_ts[proj]['flow'].mean()

    sorted_projs = printDict(UC_mean)

    return sorted_projs

def hydroPlots(policy, proj, ax_g, ax_k, col_dict, name):
    mn_g = 292120 * 10**4
    mx_g = 1470000 * 10**4
    mn_k = 76000 * 10**4
    mx_k = 570000 * 10**4
    cbar = plt.cm.get_cmap('RdBu')


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
