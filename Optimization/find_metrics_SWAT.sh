#!/bin/bash
#SBATCH --ntasks=1				# Number of tasks per serial job (must be 1)
#SBATCH -p standard				# Queue name "standard" (serial)
#SBATCH -t 9:00:00				# Run time per serial job (hh:mm:ss)
#SBATCH --mem-per-cpu=12288		# Memory per cpu (bytes)
#SBATCH --array=1-54			# Array of jobs to loop through
#SBATCH --mail-user=smj5vup@virginia.edu                                                                                                                           
#SBATCH --mail-type=ALL              

MODEL=SWAT_Omo_IrrKoysha
SEED=8
JAVA_ARGS="-cp MOEAFramework-2.13-Demo.jar"
NUM=${SLURM_ARRAY_TASK_ID}

java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator \
-d 6 -i ./MonthlyTargetOpt/objs/runtime/reference/${MODEL}_S${SEED}_step${NUM}.runref -r ./Compare_DPS_SWAT/72Hr/full_reference.ref -o ./Compare_DPS_SWAT/metrics/${MODEL}_S${SEED}_step${NUM}.metrics
