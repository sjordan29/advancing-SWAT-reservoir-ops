#/bin/bash
MODEL=Omo_IrrKoysha

python pareto.py ./sets/${MODEL}_S8.setDVO -o 125-130 -e 2.0 0.003 0.100 0.025 2300000.0 10000.0 --output ${MODEL}.referenceDVO --delimiter=" "
cut -d ' ' -f 126-131 ${MODEL}.referenceDVO >> ${MODEL}.reference