#!/bin/sh
#SBATCH --job-name="af3"
#SBATCH --partition=chorus
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=1024GB
#SBATCH --gpus=1

# User defined locations
export OUTPUT_DIR=/fh/fast/hill_g/Albert/Collaboration-TCR_Design/output1
export INPUT_DIR=/fh/fast/hill_g/Albert/Collaboration-TCR_Design/input_Test

mkdir -p $OUTPUT_DIR

# Obtaining Model Parameters
# Contact AlphaFold to get access to model parameters
#
export MODEL_PATH=/shared/biodata/alphafold3/parameter_models

#export MODEL_PATH=/home/pbradley/csdat/alphafold/af3/

export DOWNLOAD_DIR=/shared/biodata/alphafold3

SIF=/app/software/AlphaFold/containers/alpafold3.sif

apptainer exec \
  --nv \
  --bind $MODEL_PATH:/root/models \
  --bind $DOWNLOAD_DIR:/root/public_databases \
  --bind $INPUT_DIR:/root/inputs \
  --bind $OUTPUT_DIR:/root/outputs \
  $SIF \
  python /app/alphafold/run_alphafold.py \
  --input_dir=/root/inputs \
  --model_dir=/root/models \
  --db_dir=/root/public_databases \
  --output_dir=/root/outputs
