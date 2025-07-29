#!/bin/bash

# === CONFIGURATION ===
INPUT_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/INPUT/jsons_new"
MSA_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/MSAs"
TMP_DIR="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/tmp"
DB_PATH="/shared/biodata/alphafold3/uniref90"

mkdir -p "$MSA_DIR" "$TMP_DIR"

# === Loop through all JSON files ===
for json_file in "$INPUT_DIR"/*.json; do
    base=$(basename "$json_file" .json)
    fasta="${TMP_DIR}/${base}.fasta"
    msa_out="${MSA_DIR}/${base}_msa.fasta"

    # Extract chain A sequence
    seq=$(jq -r '.sequences[] | select(.protein.id=="A") | .protein.sequence' "$json_file")

    # Skip if no chain A
    if [[ -z "$seq" || "$seq" == "null" ]]; then
        echo "Skipping $base: no chain A found."
        continue
    fi

    echo "Processing $base..."

    # Write FASTA file
    echo ">${base}_A" > "$fasta"
    echo "$seq" >> "$fasta"

    # MMseqs2 pipeline
    mmseqs createdb "$fasta" "${TMP_DIR}/${base}_db"
    mmseqs search "${TMP_DIR}/${base}_db" "$DB_PATH" "${TMP_DIR}/${base}_res" "${TMP_DIR}/${base}_tmp" --threads 8
    mmseqs result2msa "${TMP_DIR}/${base}_db" "$DB_PATH" "${TMP_DIR}/${base}_res" "$msa_out"

    echo "MSA saved: $msa_out"
done
