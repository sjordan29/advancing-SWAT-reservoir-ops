module load gcc
module load anaconda

# define incoming variables
# 1: master number
# 2: NFE
i=$1
E=$2 

# change to directory
cd /scratch/smj5vup/Optimization/SWATruns/EvalM"$i"E"$E"

python prep_SWAT.py

# run SWAT
bin/swat2012.681.gfort.rel

# calculate objectives
python calc_objs.py