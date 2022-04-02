#!/bin/bash
#SBATCH -N 6
#SBATCH --ntasks-per-node 40    
#SBATCH -p parallel          				# Queue name 
#SBATCH -t 72:00:00       					# Run time (hh:mm:ss) - up to 36 hours // 1 hr for dev queue 
#SBATCH --mail-user=smj5vup@virginia.edu      # address for email notification
#SBATCH --mail-type=ALL                  	# email at Begin and End of job

module load gcc
module load openmpi
module load anaconda

make
mkdir /scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns

# SJ added 05/07/2021 - create swat folders ahead of time 
# NISLANDS is zero indexed; NCORES starts at 1
NISLANDS=1
NCORES=119
ISLANDS=$(seq 0 ${NISLANDS})
CORES=$(seq 1 ${NCORES})

for ISLAND in ${ISLANDS}
do
for CORE in ${CORES}
do 
# mkdir /scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM"$ISLAND"E"$CORE"
cp -r /scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATfiles  /scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM"$ISLAND"E"$CORE"
done
done

# Borg
srun ./mainParallel_omo_irrKoysha_SWAT.exe

# remove files 
rm -r /scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns