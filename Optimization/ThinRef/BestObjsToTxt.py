'''
Finds best policies for DPS and SWAT at step 44
Saves to text file
'''

import numpy as np 
import sys

def ncRBFpolicies(formulation):
    '''
    formulation = dps, swat, or dps_full
    '''
    # number of variables 
    if (formulation == 'dps') | (formulation == 'dps_full'):
        nvar = 125
    elif formulation == 'swat':
        nvar = 44

    # Load Pareto set
    if formulation == 'dps':
        refset = np.loadtxt('DPS_step94_thinned.referenceDVO')
    elif formulation == 'dps_full':
        refset = np.loadtxt('DPS_step94_thinned.referenceDVO')
    elif formulation =='swat':
        refset = np.loadtxt('SWAT_step94_thinned.referenceDVO')
    else:
        ("Formulation needs to be 'dps', 'dps_full', or 'swat'")
        sys.exit()
        

    # Select policy to calculate releases for - example with best hydro policy
    bestHydPt = np.argmin(refset[:,nvar]) # nvar = column with first objective value
    bestEnvFlowPt = np.argmin(refset[:,nvar+1]) # nvar+1 = column with second objective value
    bestRecAgPt = np.argmin(refset[:,nvar+2]) # nvar+2 = column with third objective value
    bestSugcPt = np.argmin(refset[:,nvar+3])
    bestCotPt = np.argmin(refset[:,nvar+4])
    
    # create a file of best points
    print(bestHydPt, bestEnvFlowPt, bestRecAgPt, bestSugcPt, bestCotPt)
    
    Hydro_u = refset[bestHydPt,:]
    EnvFlow_u = refset[bestEnvFlowPt,:]
    RecAg_u = refset[bestRecAgPt,:]
    Sugc_u = refset[bestSugcPt,:]
    Cot_u = refset[bestCotPt,:]
    
    return [Hydro_u, EnvFlow_u, RecAg_u, Sugc_u, Cot_u] 



# just print which lines
dps = ncRBFpolicies('dps')
swat = ncRBFpolicies('swat')    


# with open('DPS_bestObjs.txt', 'w') as f:
#     for item in dps:
#         for a in item:
#             f.write(str(a) + ' ')
#         f.write('\n')

# with open('SWAT_bestObjs.txt', 'w') as f:
#     for item in swat:
#         for a in item:
#             f.write(str(a) + ' ')
#         f.write('\n')