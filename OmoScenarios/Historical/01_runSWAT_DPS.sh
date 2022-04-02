#!/bin/bash
#SBATCH -D /scratch/smj5vup/omoScenarios/Historical/PythonScripts/ # working directory
#SBATCH -o /scratch/smj5vup/omoScenarios/Historical/PythonScripts/output/DPS_runSWAT.out   # Name of the output file (eg. myMPI.oJobID)
#SBATCH -N 7
#SBATCH --ntasks-per-node 14
#SBATCH -p parallel          				# Queue name "dev"
#SBATCH -A quinnlab       					# allocation name
#SBATCH -t 10:30:00       					# Run time (hh:mm:ss) - up to 36 hours // 1 hr for dev queue 
#SBATCH --mail-user=smj5vup@virginia.edu      # address for email notification
#SBATCH --mail-type=ALL                  	# email at Begin and End of job

module load gcc
module load openmpi
module load anaconda

srun python 01_runSWAT_DPS.py