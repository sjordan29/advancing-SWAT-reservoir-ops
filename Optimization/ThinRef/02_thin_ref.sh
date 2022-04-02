MODEL=DPS_step94
python pareto.py ./${MODEL}.setDVO -o 125-129 -e 8.0 0.03 1.000 3800000.0 150000.0 --output ${MODEL}_thinned.referenceDVO --delimiter=" "
cut -d ' ' -f 126-130 ${MODEL}_thinned.referenceDVO >> ${MODEL}_thinned.reference

MODEL=SWAT_step94
python pareto.py ./${MODEL}.setDVO -o 44-48 -e 8.0 0.03 1.000 3800000.0 150000.0  --output ${MODEL}_thinned.referenceDVO --delimiter=" "
cut -d ' ' -f 45-49 ${MODEL}_thinned.referenceDVO >> ${MODEL}_thinned.reference

## Note: make sure all pound signs/empty lines at the bottom of the setDVO files are gone or this will fail. 