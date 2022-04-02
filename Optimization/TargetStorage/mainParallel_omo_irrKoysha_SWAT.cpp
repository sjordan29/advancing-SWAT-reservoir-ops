 //============================================================================
// Name        : mainParallel_omo_irrKoysha.cpp
// Author      : MatteoG
// Version     :
// Copyright   : Your copyright notice
//============================================================================

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <math.h>
#include <fstream>
#include "borgmm.h"
#include <iostream>


using namespace std;

int nvars = 44; // 13 per reservoir * 3 reservoirs, plus 5 irrigation 
int nobjs = 5; // hydropower, environmental flows, flood recession ag, sugarcane yield, cotton yield
int nconstr = 1; // flows can't exceed historical maximum 

// function for reading in objectives - assumes one objective per row
void loadArray(string file_name, unsigned int l, double *pArray){
    double x;
    ifstream input(file_name.c_str(), ifstream::in);
    //ifstream input(file_name);
    if (input.is_open()){
        for(unsigned int i = 0; i<l; i++){
            input >> x;
            pArray[i] = x;
        }
        input.close();
    }
    else cout << "Unable to open file1";
}

void model_wrapper(double *vars, double *objs, double *constr, int *evals, int *isle, int*worker)
{
    // Create a new directory to hold the SWAT files for this evaluation number
    char command[256];
    unsigned int inum = *isle;
    unsigned int E = *evals;
    unsigned int fld = *worker; // SJ added 05/10/2021 
    // copy SWAT files to the new directory
    // sprintf(command, "cp -r /project/quinnlab/smj5vup/Optimization/MonthlyTargetOpt/SWATfiles /project/quinnlab/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM%uE%u", inum, E); // correct SWATfiles path name
    // system(command);

    // write decision variables to a file in the new directory
    char vars_file_name[256];
    // sprintf(vars_file_name, "/project/quinnlab/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM%uE%u/vars_file.txt", inum, E); // change to what you call the file SWAT reads in
    sprintf(vars_file_name, "/scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM%uE%u/vars_file.txt", inum, fld); // SJ modified 05/07/2021 -- change to folder
    FILE * vars_file = NULL;
    vars_file = fopen(vars_file_name, "a");
    for(int i=0; i<nvars; i++){
        fprintf(vars_file, "%f\n", vars[i]); // write decision variable to file
    }
    fclose(vars_file);
    

    // call Python script that rearranges var file, changes irrigation parameters
    // sprintf(command, "sh runSWAT.sh %u %u", inum, E);
    sprintf(command, "sh runSWAT.sh %u %u", inum, fld); // SJ 05/07/2021 -- pass folder name 
    system(command);
    

    // read in objectives
    char objs_file_name[256];
    sprintf(objs_file_name, "/scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM%uE%u/objs_file.txt", inum, fld); // correct objectives file name
    loadArray(objs_file_name, nobjs, objs); // not working; try something else 


    // read constraint
    char constr_file_name[256];
    sprintf(constr_file_name, "/scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM%uE%u/constraint.txt", inum, fld);
    loadArray(constr_file_name, nconstr, constr);
    

    // delete files
//     sprintf(command, "rm -r /project/quinnlab/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM%uE%u", inum, E);
//     system(command);

     sprintf(command, "rm /scratch/smj5vup/Optimization/MonthlyTargetOpt/SWATruns/EvalM%uE%u/vars_file.txt", inum, fld);
     system(command);
     
 }

int main(int argc, char* argv[]) {
	// BORG_Debug_on();
    //feenableexcept(FE_INVALID | FE_OVERFLOW | FE_DIVBYZERO);

    // setting random seed
    unsigned int seed = 8; // hard coded -- Jared
    srand(seed);

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // Changes for MPI version start here
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    BORG_Algorithm_ms_startup(&argc, &argv);
    BORG_Algorithm_ms_islands(2);

    //Enable global Latin hypercube initialization to ensure each island
    // gets a well sampled distribution of solutions.
    BORG_Algorithm_ms_initialization(INITIALIZATION_LATIN_GLOBAL);

    BORG_Algorithm_ms_max_time(71.30); // SJ updated 
    // BORG_Algorithm_ms_max_time(0.125); // SJ updated 
    BORG_Algorithm_output_frequency(1000); // SJ updated 

    // Define the problem with decisions, objectives, constraints, and the evaluation function
    BORG_Problem problem = BORG_Problem_create(nvars, nobjs, nconstr, model_wrapper);

    // Set parameter bounds for irrigation decision variables - change to SWAT irrigation vars
    BORG_Problem_set_bounds(problem, 0, 0.0, 1.0); // auto-stress value for District 1
    BORG_Problem_set_bounds(problem, 1, 0.0, 100.0); // irr_mx for District 1
    BORG_Problem_set_bounds(problem, 2, 0.0, 1.0); // auto-stress value for District 2
    BORG_Problem_set_bounds(problem, 3, 0.0, 100.0); // irr_mx for District 2
    BORG_Problem_set_bounds(problem, 4, 1.0, 2.0); // wstrs_id for Districts 1 and 2 (1 means plant wanter demand; 2 means soil water demand)

    // Set parameter bounds Gibe I 
    for(int i=5; i<17; i++){
        BORG_Problem_set_bounds(problem, i, 17437.0, 80213.0); // min and max reservoir volume for GI 
    }
    BORG_Problem_set_bounds(problem, 17, 1, 30); // NDTARGR for Gibe I
    
    // Set parameter bounds for Gibe III 
    for(int i=18; i<30; i++){
        BORG_Problem_set_bounds(problem, i, 292120.0, 1470000.0); // min and max reservoir volume for GIII  
    }
    BORG_Problem_set_bounds(problem, 30, 1, 30); // NDTARGR for Gibe III


// Set parameter bounds for Koysha
    for(int i=31; i<43; i++){
        BORG_Problem_set_bounds(problem, i, 76000.0, 570000.0); // min and max reservoir volume for koysha
    }

    BORG_Problem_set_bounds(problem, 43, 1, 30); // NDTARGR for Koysha

    // Set epsilons for objectives
    BORG_Problem_set_epsilon(problem, 0, 2.0); // hydropower epsilon
    BORG_Problem_set_epsilon(problem, 1, 0.01); // environmental flow epsilon 
    BORG_Problem_set_epsilon(problem, 2, 0.30); // recession agriculture epsilon
    BORG_Problem_set_epsilon(problem, 3, 1260000.0); // sugar cane epsilon 
    BORG_Problem_set_epsilon(problem, 4, 41000.0); // cotton epsilon

    // This is set up to run only one seed at a time.
    char outputFilename[256];
    char runtime[256];
    FILE* outputFile = NULL;
    sprintf(outputFilename, "/scratch/smj5vup/Optimization/MonthlyTargetOpt/sets/Omo_IrrKoysha_S%d.set", seed); // output path (make sure this exists) -- in optimization folder (SJ)
    sprintf(runtime, "/scratch/smj5vup/Optimization/MonthlyTargetOpt/runtime/Omo_IrrKoysha_S%d_M%%d.runtime", seed); // runtime path (make sure this exists) -- in optimization folder (SJ)

    BORG_Algorithm_output_runtime(runtime);

    int rank; // different seed on each processor
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    BORG_Random_seed(37*seed*(rank+1));
    BORG_Archive result = BORG_Algorithm_ms_run(problem); // this actually runs the optimization

    // If this is the master node, print out the final archive
    if (result != NULL) {
        outputFile = fopen(outputFilename, "w");
        if (!outputFile) {
            BORG_Debug("Unable to open final output file\n");
        }
        BORG_Archive_print(result, outputFile);
        BORG_Archive_destroy(result);
        fclose(outputFile);
    }

    BORG_Algorithm_ms_shutdown();
    BORG_Problem_destroy(problem);


    return EXIT_SUCCESS;

}