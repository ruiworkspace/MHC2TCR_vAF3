#!/bin/bash

# Define paths
INPUT_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/INPUT/jsons_new"
MSA_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/MSAs"
DB_PATH="/shared/biodata/alphafold3/uniref90"
mkdir -p "$MSA_DIR"

ml MMseqs2  # or use conda if needed

# Loop through all JSON input files
for json_file in "$INPUT_DIR"/*.json; do
    base=$(basename "$json_file" .json)
    fasta="/tmp/${base}.fasta"
    msa_out="${MSA_DIR}/${base}_msa.fasta"

    # Extract the sequence from the JSON
    seq=$(jq -r '.targets[0].sequence' "$json_file")
    echo ">${base}" > "$fasta"
    echo "$seq" >> "$fasta"

    # Generate MSA using MMseqs2
    mmseqs createdb "$fasta" input_db
    mmseqs search input_db "$DB_PATH" result_db tmp_dir --threads 8
    mmseqs result2msa input_db "$DB_PATH" result_db "$msa_out"

    echo "✅ MSA written to $msa_out"
done
