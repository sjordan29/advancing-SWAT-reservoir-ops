#!/bin/bash
#SBATCH -N 1
#SBATCH -p standard        				# Queue name "dev"
#SBATCH -t 5:30:00       					# Run time (hh:mm:ss) - up to 36 hours // 1 hr for dev queue 
#SBATCH --mail-user=smj5vup@virginia.edu      # address for email notification
#SBATCH --mail-type=ALL                  	# email at Begin and End of job



python 12_ReservoirTimeseries.py 