import pandas as pd
import numpy as np
from Hydropower import *
from Flows import *
from Yield import *


### HYDROPOWER ########################################################
def HydroObj(TxtFold, dates):
	df = calcHydropower(TxtFold + 'output.rsv', dates)
	years = np.unique(df.year)
	hydObj = df.hydropower.sum() / len(years) / 1000 * -1 # matteo divides by 1000 : GWh
	return hydObj

### ENV FLOWS & RECESSION ############################################
def RecEnvObj(ra, ef, ra_targ, ef_targ, dates):
	# recession objective 
	# ra, ef = calcFlows(TxtFold + '/output.rch', dates)
	ra_merge = mergeRegimes(ra, ra_targ)
	rec = RecObj(ra_merge)
	# environmental flows 
	ef_merge = mergeRegimes(ef, ef_targ)
	env = EnvObj(ef_merge)
	return rec, env 


### YIELD ##############################################################
def YieldObj(TxtFold, dates):
	s, c = calcYld(TxtFold + 'output.hru', dates)
	sugObj = (s.s1_kg.sum() + s.s2_kg.sum() + s.s3_kg.sum()) / len(s.s1_kg)
	cotObj = (c.c1_kg.sum() + c.c2_kg.sum()) / len(c.c1_kg)
	return sugObj, cotObj


def calcObjs(TxtFold):
	dates = pd.date_range(start="1989-01-01",end="2018-12-31", freq='d')

	# hydropower
	hyd_obj = HydroObj(TxtFold, dates)

	# flows 
	ra, ef = calcFlows(TxtFold + 'output.rch', dates)

	# recession setup 
	yr_dates = pd.date_range(start="1989-01-01",end="1989-12-31", freq='d')
	fr = pd.read_csv('RA_Targs.csv',header=None) # change file location
	fr.columns = ['date','targ']
	ra_targ = pd.DataFrame({'month': yr_dates.month, 'day': yr_dates.day, 'targ':fr['targ']})

	# environmental flows setup 
	ef_t = pd.read_csv('omorateRegime.txt', sep='\t',header=None)
	ef_targ = pd.DataFrame({'month': yr_dates.month, 'day': yr_dates.day, 'flow':ef_t.values[0]})

	# rec + env 
	rec_obj, env_obj = RecEnvObj(ra, ef, ra_targ, ef_targ, dates)
	env_obj = env_obj/1000000 # (m3/s)^2/10^6 -- matteo
	rec_obj = rec_obj/10/1000 # (m3/s)^2/10^4  -- matteo

	# yield 
	sug_obj,cot_obj = YieldObj(TxtFold,dates)
	sug_obj = sug_obj * -1 # negative bc we want to maximize yields
	cot_obj = cot_obj * -1 # negative bc we want to maximize yields

	# write to file 
	f = open("objs_file.txt", "w")
	for item in [hyd_obj, env_obj, rec_obj, sug_obj, cot_obj]:
		f.write("%s\n" % str(item))
	f.close()

	# constraint 
	constraint = max(ra.flow.max()-3290, 0)

	with open("constraint.txt", "w") as f:
		f.write(str(constraint))
		
calcObjs("")