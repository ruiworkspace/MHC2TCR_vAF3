#!/bin/bash
#SBATCH --job-name="af3_msa"
#SBATCH --partition=chorus
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=1024GB
#SBATCH --gpus=1

export INPUT_JSON="$1"
BASE=$(basename "$INPUT_JSON" .json)

export INPUT_DIR=/fh/fast/hill_g/Albert/Collaboration-TCR_Design/input_Test
export OUTPUT_DIR=/fh/fast/hill_g/Albert/Collaboration-TCR_Design/output1/$BASE
export MSA_DIR=/fh/fast/hill_g/Rui/mhc2tcr_2507/MSAs
export MODEL_PATH=/shared/biodata/alphafold3/parameter_models
export DOWNLOAD_DIR=/shared/biodata/alphafold3
export TMP_DIR=/fh/fast/hill_g/Rui/mhc2tcr_2507/tmp/$BASE

mkdir -p "$OUTPUT_DIR" "$TMP_DIR"

MSA_A="${MSA_DIR}/${BASE}_chainA_msa.fasta"
MSA_B="${MSA_DIR}/${BASE}_chainB_msa.fasta"

if [[ ! -s "$MSA_A" || ! -s "$MSA_B" ]]; then
    echo "Missing MSA for $BASE; expected files:"
    echo "  $MSA_A"
    echo "  $MSA_B"
    exit 1
fi

SIF=/app/software/AlphaFold/containers/alpafold3.sif

apptainer exec \
  --nv \
  --bind $MODEL_PATH:/root/models \
  --bind $DOWNLOAD_DIR:/root/public_databases \
  --bind $INPUT_DIR:/root/inputs \
  --bind $OUTPUT_DIR:/root/outputs \
  --bind $MSA_DIR:/root/msas \
  --bind $TMP_DIR:/root/tmp \
  $SIF \
  python /app/alphafold/run_alphafold.py \
  --input_json=/root/inputs/$(basename "$INPUT_JSON") \
  --model_dir=/root/models \
  --db_dir=/root/public_databases \
  --output_dir=/root/outputs \
  --tmp_dir=/root/tmp \
  --msa_chain_a=/root/msas/${BASE}_chainA_msa.fasta \
  --msa_chain_b=/root/msas/${BASE}_chainB_msa.fasta
