'''
Figures out which policies are in combined pareto set 
'''

import numpy as np 
import sys

dps =  np.loadtxt('DPS_step94_thinned.reference')
swat =  np.loadtxt('SWAT_step94_thinned.reference')
combo = np.loadtxt('thin_reference.ref')

DPS_indices = []
SWAT_indices = []

for x in combo:
    ismemberDPS = [row[-5:]==x for row in dps.tolist()]
    ismemberSWAT = [row[-5:]==x for row in swat.tolist()]

    dps_vals = np.where(ismemberDPS)[0].tolist()
    swat_vals = np.where(ismemberSWAT)[0].tolist()

    if len(dps_vals) > 0:
        DPS_indices.append(dps_vals)
    if len(swat_vals) > 0:
        SWAT_indices.append(swat_vals)


flat_DPS = np.unique([item for sublist in DPS_indices for item in sublist]).tolist()
flat_SWAT = np.unique([item for sublist in SWAT_indices for item in sublist]).tolist()


print("----------------DPS--------------------")
print(len(flat_DPS))
print(flat_DPS)
print("--------------SWAT--------------------")
print(len(flat_SWAT))
print(flat_SWAT)


# find best policy each objective from SWAT 
d = dps[flat_DPS]
nvar= 0
bestHydPt = np.argmin(d[:,nvar]) # nvar = column with first objective value
bestEnvFlowPt = np.argmin(d[:,nvar+1]) # nvar+1 = column with second objective value
bestRecAgPt = np.argmin(d[:,nvar+2]) # nvar+2 = column with third objective value
bestSugcPt = np.argmin(d[:,nvar+3])
bestCotPt = np.argmin(d[:,nvar+4])


Hydro_u = d[bestHydPt,0]
EnvFlow_u = d[bestEnvFlowPt,1]
RecAg_u = d[bestRecAgPt,2]
Sugc_u = d[bestSugcPt,3]
Cot_u = d[bestCotPt,4]

bestHydPol = np.where([row[nvar]==Hydro_u for row in dps.tolist()])
bestEnvPol = np.where([row[nvar+1]==EnvFlow_u for row in dps.tolist()])
bestRecPol = np.where([row[nvar+2]==RecAg_u for row in dps.tolist()])
bestSugPol = np.where([row[nvar+3]==Sugc_u for row in dps.tolist()])
bestCotPol = np.where([row[nvar+4]==Cot_u for row in dps.tolist()])


print(bestHydPol, bestEnvPol, bestRecPol, bestSugPol, bestCotPol)

s = swat[flat_SWAT]
bestHydPt = np.argmin(s[:,nvar]) # nvar = column with first objective value
bestEnvFlowPt = np.argmin(s[:,nvar+1]) # nvar+1 = column with second objective value
bestRecAgPt = np.argmin(s[:,nvar+2]) # nvar+2 = column with third objective value
bestSugcPt = np.argmin(s[:,nvar+3])
bestCotPt = np.argmin(s[:,nvar+4])
print(bestHydPt, bestEnvFlowPt, bestRecAgPt, bestSugcPt, bestCotPt)



Hydro_u = s[bestHydPt,0]
EnvFlow_u = s[bestEnvFlowPt,1]
RecAg_u = s[bestRecAgPt,2]
Sugc_u = s[bestSugcPt,3]
Cot_u = s[bestCotPt,4]

bestHydPol = np.where([row[nvar]==Hydro_u for row in swat.tolist()])
bestEnvPol = np.where([row[nvar+1]==EnvFlow_u for row in swat.tolist()])
bestRecPol = np.where([row[nvar+2]==RecAg_u for row in swat.tolist()])
bestSugPol = np.where([row[nvar+3]==Sugc_u for row in swat.tolist()])
bestCotPol = np.where([row[nvar+4]==Cot_u for row in swat.tolist()])

print(bestHydPol, bestEnvPol, bestRecPol, bestSugPol, bestCotPol)
