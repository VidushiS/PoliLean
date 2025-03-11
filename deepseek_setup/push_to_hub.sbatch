#!/bin/bash
# Script for launching model profiling

#SBATCH -J profile_model           # Job name
#SBATCH -o job.%j.out         # Name of stdout output file (%j expands to jobId)
#SBATCH -N 1                  # Total number of nodes requested
#SBATCH -t 00:30:00           # Run time (hh:mm:ss) - 0.5 hours
#SBATCH -p devel              # Desired partition
module load pytorch
cd $WORK/PoliLean/deepseek_setup


HIP_VISIBLE_DEVICES="0,1,2,3" python push_files_to_hub.py >& job.${SLURM_JOB_ID}_base_deepseek.out 
