'''
Sarah Jordan
05/24/2021

move objectives file
'''


from mpi4py import MPI
import os 
import sys
import numpy as np


class Unbuffered:
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def mkdir_p(path):
    '''
    https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def run_SWAT(file, rank, dir_name):
    os.chdir(file)
    if len(str(rank)) < 2:
        rank = "0" + str(rank)

    os.chdir("TxtInOut_%s/SWATfiles" % rank) # change to directory
    
    # copy files
    obj_name = "P_" + str(rank) + "_objs.txt"
    os.system("cp objs_file.txt /scratch/smj5vup/omoScenarios/Historical/Objectives/%s/%s" % (dir_name, obj_name))


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
if rank <= 97:
    run_SWAT('/scratch/smj5vup/omoScenarios/Historical/DPS/', rank, "DPS")
if rank <= 60:
    run_SWAT('/scratch/smj5vup/omoScenarios/Historical/SWAT', rank, "SWAT")
