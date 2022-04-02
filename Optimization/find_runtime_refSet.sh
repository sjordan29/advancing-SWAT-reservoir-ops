#/bin/bash
MODEL=DPS_Omo_IrrKoysha
SEED=8
NSTEPS=65
STEPS=$(seq 0 ${NSTEPS})

for STEP in ${STEPS}
do
	python pareto.py ./objs/runtime/${MODEL}_S${SEED}_M*/*_step${STEP}.obj -o 0-5 -e 2.0 0.003 0.100 0.025 2300000.0 10000.0\
	--output ./objs/runtime/reference/${MODEL}_S${SEED}_step${STEP}.runref --delimiter=" " --comment="#" --blank
	python pareto.py ./runtime/${MODEL}_S${SEED}_M*/*_step${STEP}.set -o 125-130 -e 2.0 0.003 0.100 0.025 2300000.0 10000.0\
	--output ./runtime/reference/${MODEL}_S${SEED}_step${STEP}.runset --delimiter=" " -c "#" "//" --blank
done
