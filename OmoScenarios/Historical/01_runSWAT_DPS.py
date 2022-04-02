'''
Sarah Jordan
05/24/2021

Run all DPS scenarios and calculate objectives under historical conditions.
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
    if os.path.exists('TxtInOut_%s' % rank):
        print("skipping", file)
        pass 
    else:
        mkdir_p('TxtInOut_%s' % rank) # make directory
        os.system('cp -r SWATfiles TxtInOut_%s' % rank) #copy swat files 
        os.chdir("TxtInOut_%s/SWATfiles" % rank) # change to directory
        os.system("python prep_SWAT.py %s" % rank) # update mgt files
        os.system("/scratch/smj5vup/SourceCodeChanges/SpeedUpSWAT/bin/swat2012.681.gfort.rel") # run swat

        # calculate objectives 
        os.system("python calc_objs.py") 


        os.system("python hru.py") # get cotton and sugc file

        os.system("rm output.hru") # remove hru file 
        os.system("rm 0*") # remove unnecessary files 
        os.system("rm *.wwq*") # remove unnecessary files 
        os.system("rm *.dat") # remove unnecessary files 
        os.system("rm *.ATM") # remove unnecessary files 
        os.system("rm *.deg") # remove unnecessary files 
        os.system("rm bmp*") # remove unnecessary files 
        os.system("rm *.cst") # remove unnecessary files 
        os.system("rm *.ini") # remove unnecessary files 
        os.system("rm *.bsn") # remove unnecessary files 
        os.system("rm fig.fig") # remove unnecessary files 
        os.system("rm *.qst") # remove unnecessary files 
        os.system("rm *.sh") # remove unnecessary files 
        os.system("rm file.cio") # remove unnecessary files  
        os.system("rm fin.fin") # remove unnecessary files 
        os.system("rm input.std") # remove unnecessary files 
        os.system("rm output.pst") # remove unnecessary files 
        # remove more files 
        os.system("rm max_release*")
        os.system("rm lsv*")
        os.system("rm omorateRegime.txt")
        os.system("rm hyd.out")
        os.system("rm *.py")
        os.system("rm r.txt")
        os.system("rm ra.txt")
        os.system("rm w.txt")
        os.system("rm irr.txt")
        os.system("rm tmp1.tmp")
        os.system("rm pcp1.pcp")
        os.system("rm RA_Targs.csv")
        os.system("rm output.sed")
        # copy files
        obj_name = file + "_" + str(rank) + "_objs.txt"
        os.system("cp objs_file.txt /scratch/smj5vup/omoScenarios/Historical/Objectives/%s/%s" % (dir_name, obj_name))


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
if rank <= 97:
    run_SWAT('/scratch/smj5vup/omoScenarios/Historical/DPS/', rank, "DPS")
if rank <= 60:
    run_SWAT('/scratch/smj5vup/omoScenarios/Historical/SWAT', rank, "SWAT")
