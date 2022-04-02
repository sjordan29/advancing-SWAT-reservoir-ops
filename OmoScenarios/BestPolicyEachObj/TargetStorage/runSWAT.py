from mpi4py import MPI
import os 
# import sys

import sys
import numpy as np

def mkdir_p(path):
    '''
    https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
    '''
    if not os.path.exists(path):
        os.makedirs(path)


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
rank = rank  # starts at 0 and my folders start at 1 

if rank < 5:
	mkdir_p('TxtInOut_%s' % rank) # make directory
	os.system('cp -r SWATfiles TxtInOut_%s' % rank) #copy swat files 
	os.chdir("TxtInOut_%s/SWATfiles" % rank) # change to directory
	os.system("python prep_SWAT.py %s" % rank) # update mgt files
	os.system("/project/quinnlab/smj5vup/SourceCodeChanges/SpeedUpSWAT/bin/swat2012.681.gfort.rel") # run swat
	# os.system('bin/swat2012.681.gfort.rel')
	os.system("python calc_objs.py") # calculate objectives 
	os.system("rm 0*")