#!/bin/bash

# === CONFIGURATION ===
JSON_DIR="/fh/fast/hill_g/Rui/mhc2tcr_2507/INPUT/jsons_new/"
TMP_DIR="/fh/fast/hill_g/Rui/mhc2tcr_2507/single_test1/tmp"
FASTA_DIR="$TMP_DIR/fasta"
DB_DIR="$TMP_DIR/db"
RES_DIR="$TMP_DIR/results"
MSADB_DIR="$TMP_DIR/msa_db"
MSA_DIR="/fh/fast/hill_g/Rui/mhc2tcr_2507/single_test1/MSAs"
UNIREF_DB="/fh/fast/hill_g/Rui/MHC2TCR_test_250722/uniref90_mmseqs_db"

mkdir -p "$FASTA_DIR" "$DB_DIR" "$RES_DIR" "$MSADB_DIR" "$MSA_DIR"

# === LOAD MMseqs2 ===
module --ignore_cache load MMseqs2/13-45111-gompi-2021b || {
  echo "Failed to load MMseqs2 module" >&2
  exit 1
}

# === PROCESS JSON FILES ===
for json in "$JSON_DIR"/*.json; do
    base=$(basename "$json" .json)
    echo "Processing $base"

    for chain in A B; do
        seq=$(jq -r --arg ID "$chain" '.sequences[] | select(.protein.id==$ID) | .protein.sequence' "$json")

        if [[ -z "$seq" || "$seq" == "null" ]]; then
            echo "No sequence found for chain $chain in $base"
            continue
        fi

        fasta="$FASTA_DIR/${base}_chain${chain}.fasta"
        db="$DB_DIR/${base}_chain${chain}_db"
        res="$RES_DIR/${base}_chain${chain}_res"
        msa_db="$MSADB_DIR/${base}_chain${chain}_msa_db"
        msa="$MSA_DIR/${base}_chain${chain}.a3m"
        tmp="$TMP_DIR/${base}_chain${chain}_tmp"

        echo ">${base}_chain${chain}" > "$fasta"
        echo "$seq" >> "$fasta"

        mmseqs createdb "$fasta" "$db"
        mmseqs linsearch "$db" "$UNIREF_DB" "$res" "$tmp" --threads 8

        mmseqs result2msa "$db" "$UNIREF_DB" "$res" "$msa_db" \
            --msa-format-mode 0 \
            --max-seq-id 1.0 \
            --qid 0.0 \
            --cov 0.0 \
            --threads 8

        mmseqs convertmsa "$db" "$msa_db" "$msa" --format-output-mode 2

        echo "MSA written: $msa"
    done
done
