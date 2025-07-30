#!/bin/bash
#SBATCH --job-name=af3
#SBATCH --partition=chorus
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=1024GB
#SBATCH --gpus=1

# === Environment Setup ===
INPUT_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/INPUT/jsons_new"
OUTPUT_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/OUTPUT"
MSA_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/MSAs"
MODEL_PATH="/shared/biodata/alphafold3/parameter_models"
DOWNLOAD_DIR="/shared/biodata/alphafold3"
SIF="/app/software/AlphaFold/containers/alpafold3.sif"

mkdir -p "$OUTPUT_DIR"

# === Main Loop ===
for json in "$INPUT_DIR"/*.json; do
    name=$(basename "$json" .json)

    # Paths to MSA files for chain A and chain B
    msa_a="${MSA_DIR}/${name}_chainA_msa.fasta"
    msa_b="${MSA_DIR}/${name}_chainB_msa.fasta"

    # Check if MSA files exist
    if [[ ! -s "$msa_a" || ! -s "$msa_b" ]]; then
        echo "Missing MSA for $name; skipping..."
        continue
    fi

    # === Run AlphaFold 3 ===
    apptainer exec \
      --nv \
      --bind "$MODEL_PATH:/root/models" \
      --bind "$DOWNLOAD_DIR:/root/public_databases" \
      --bind "$json:/root/input.json" \
      --bind "$OUTPUT_DIR:/root/outputs" \
      --bind "$msa_a:/root/msa_chainA.fasta" \
      --bind "$msa_b:/root/msa_chainB.fasta" \
      "$SIF" \
      python /app/alphafold/run_alphafold.py \
      --input_json=/root/input.json \
      --msa_paths=/root/msa_chainA.fasta,/root/msa_chainB.fasta \
      --model_dir=/root/models \
      --db_dir=/root/public_databases \
      --output_dir=/root/outputs/${name}

    echo "Finished: $name"
done
