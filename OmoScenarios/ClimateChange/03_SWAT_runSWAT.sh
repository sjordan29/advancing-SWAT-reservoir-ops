#!/bin/bash
#SBATCH -N 3
#SBATCH --ntasks-per-node 20
#SBATCH -p parallel          				# Queue name "dev"
#SBATCH -t 20:30:00       					# Run time (hh:mm:ss) - up to 36 hours // 1 hr for dev queue 
#SBATCH --mail-user=smj5vup@virginia.edu      # address for email notification
#SBATCH --mail-type=ALL                  	# email at Begin and End of job

module load gcc
module load openmpi
module load anaconda

srun python 03_SWAT_runSWAT.py