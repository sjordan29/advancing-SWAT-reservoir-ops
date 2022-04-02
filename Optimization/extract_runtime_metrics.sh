#!/bin/bash
MODEL=GInolic
SEED=7
JAVA_ARGS="-cp MOEAFramework-2.13-Demo.jar"

ISLE=0
java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ExtractData \
-d 3 -i ./runtime/${MODEL}_S${SEED}_M${ISLE}.runtime -r ${MODEL}.reference \
-o ./metrics/runtime/${MODEL}_S${SEED}_M${ISLE}.data NFE ElapsedTime SBX DE PCX SPX UNDX UM Improvements Restarts PopulationSize ArchiveSize MutationIndex HelpRequests

ISLE=1
java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ExtractData \
-d 3 -i ./runtime/${MODEL}_S${SEED}_M${ISLE}.runtime -r ${MODEL}.reference \
-o ./metrics/runtime/${MODEL}_S${SEED}_M${ISLE}.data NFE ElapsedTime SBX DE PCX SPX UNDX UM Improvements Restarts PopulationSize ArchiveSize MutationIndex HelpRequests