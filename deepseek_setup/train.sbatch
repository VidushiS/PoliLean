#!/bin/bash
# Script for launching model profiling

#SBATCH -J profile_model           # Job name
#SBATCH -o job.%j.out         # Name of stdout output file (%j expands to jobId)
#SBATCH -N 1                  # Total number of nodes requested
#SBATCH -t 12:30:00           # Run time (hh:mm:ss) - 0.5 hours
#SBATCH -p mi2104x          # Desired partition
module load pytorch
cd $WORK/PoliLean/deepseek_setup


#HIP_VISIBLE_DEVICES="0,1,2,3" python train_deepseek.py >& job.${SLURM_JOB_ID}.out 
HIP_VISIBLE_DEVICES="0,1,2,3" python -m torch.distributed.launch --nproc-per-node=4 --nnodes=1 train_deepseek.py --data-file ./partisan_news_gdown/BIGNEWSBLN_left_text_array.json --output-dir ./news_left_deepseek --percent 4 >& job.${SLURM_JOB_ID}.out
