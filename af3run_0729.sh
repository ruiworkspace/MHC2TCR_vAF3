#!/bin/bash
#SBATCH --job-name=af3
#SBATCH --partition=chorus
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=1024GB
#SBATCH --gpus=1

# === Load MMseqs2 ===
ml MMseqs2/13-45111-gompi-2021b

# === Set paths ===
INPUT_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/INPUT/jsons_new"
OUTPUT_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/OUTPUT"
MSA_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/MSAs"
MODEL_PATH="/shared/biodata/alphafold3/parameter_models"
DOWNLOAD_DIR="/shared/biodata/alphafold3"
SIF="/app/software/AlphaFold/containers/alpafold3.sif"

mkdir -p "$MSA_DIR"

# === Loop through JSON files ===
for json in "$INPUT_DIR"/*.json; do
    name=$(basename "$json" .json)
    fasta="/tmp/${name}.fasta"

    # === Extract sequence from JSON ===
    seq=$(jq -r '.targets[0].sequence' "$json")
    echo ">${name}" > "$fasta"
    echo "$seq" >> "$fasta"

    # === Generate MSA using MMseqs2 ===
    mmseqs createdb "$fasta" input_db
    mmseqs search input_db /shared/biodata/alphafold3/uniref90 result_db tmp_dir --threads 8
    mmseqs result2msa input_db /shared/biodata/alphafold3/uniref90 result_db "${MSA_DIR}/${name}_msa.fasta"

    # === Run AF3 with MSA ===
    apptainer exec \
      --nv \
      --bind "$MODEL_PATH:/root/models" \
      --bind "$DOWNLOAD_DIR:/root/public_databases" \
      --bind "$json:/root/input.json" \
      --bind "$OUTPUT_DIR:/root/outputs" \
      --bind "$MSA_DIR:/root/msas" \
      "$SIF" \
      python /app/alphafold/run_alphafold.py \
      --input_json=/root/input.json \
      --msa_path="/root/msas/${name}_msa.fasta" \
      --model_dir=/root/models \
      --db_dir=/root/public_databases \
      --output_dir=/root/outputs/${name}
done
