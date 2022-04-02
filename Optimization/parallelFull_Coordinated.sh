#!/bin/bash
#SBATCH -N 6
#SBATCH --ntasks-per-node 40
#SBATCH -p parallel          				# Queue name 
#SBATCH -t 72:00:00       					# Run time (hh:mm:ss) 
#SBATCH --mail-user=smj5vup@virginia.edu      # address for email notification
#SBATCH --mail-type=ALL                  	# email at Begin and End of job

module load gcc
module load openmpi
module load anaconda

make
mkdir /scratch/smj5vup/Optimization/SWATruns

srun ./mainParallel_omo_irrKoysha.exe