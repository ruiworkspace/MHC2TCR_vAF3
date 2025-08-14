import os
import re
import pandas as pd
from typing import List, Tuple

# Path to your input file
in_path = "/YOUR/PATH/TO/refdata-cellranger-vdj-GRCm38-alts-ensembl-7.0.0/fasta/regions.fa"

# === Provide your list of gene names here ===
gene_names: List[str] = ["TRBJ1-1", "TRBJ1-2", "TRBJ1-3", "TRBJ1-4", "TRBJ1-5", "TRBJ2-1", "TRBJ2-2", "TRBJ2-3", "TRBJ2-4", "TRBJ2-5", "TRBJ2-7"] #replace with the TRAV/TRBV you would like to search

# Precompile search regexes for speed/robustness (exact token between pipes)
gene_regexes = {g: re.compile(rf"\|{re.escape(g)}\|") for g in gene_names}
need_phrase = "J-REGION"

# Standard genetic code
CODON_TABLE = {
    "TTT":"F","TTC":"F","TTA":"L","TTG":"L","CTT":"L","CTC":"L","CTA":"L","CTG":"L",
    "ATT":"I","ATC":"I","ATA":"I","ATG":"M","GTT":"V","GTC":"V","GTA":"V","GTG":"V",
    "TCT":"S","TCC":"S","TCA":"S","TCG":"S","AGT":"S","AGC":"S","CCT":"P","CCC":"P",
    "CCA":"P","CCG":"P","ACT":"T","ACC":"T","ACA":"T","ACG":"T","GCT":"A","GCC":"A",
    "GCA":"A","GCG":"A","TAT":"Y","TAC":"Y","CAT":"H","CAC":"H","CAA":"Q","CAG":"Q",
    "AAT":"N","AAC":"N","AAA":"K","AAG":"K","GAT":"D","GAC":"D","GAA":"E","GAG":"E",
    "TGT":"C","TGC":"C","TGG":"W","CGT":"R","CGC":"R","CGA":"R","CGG":"R","AGA":"R",
    "AGG":"R","GGT":"G","GGC":"G","GGA":"G","GGG":"G","TAA":"*","TAG":"*","TGA":"*"
}

def translate(seq_nt: str) -> Tuple[str, str]:
    """Translate nucleotide string from first base; return (aa, leftover_nt)."""
    s = re.sub(r"[^ACGTNacgtn]", "", seq_nt).upper()
    aa = []
    for i in range(0, len(s) - len(s) % 3, 3):
        codon = s[i:i+3]
        aa.append(CODON_TABLE.get(codon, "X"))
    leftover = s[len(s) - (len(s) % 3):] if (len(s) % 3) != 0 else ""
    return "".join(aa), leftover

# Read alternating lines: name, sequence
with open(in_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = [ln.strip() for ln in f if ln.strip()]

pairs = [(lines[i], lines[i+1]) for i in range(0, len(lines)-1, 2)]

filtered_rows = []
found_genes = set()

for name, seq in pairs:
    if need_phrase in name:
        matched_gene = None
        for g, rx in gene_regexes.items():
            if rx.search(name):
                matched_gene = g
                found_genes.add(g)
                break
        if matched_gene:
            aa, leftover = translate(seq)
            filtered_rows.append({
                "gene_name": matched_gene,
                "sequence_nt": seq,
                "translation_aa": aa,
                "leftover_nt": leftover
            })

# Save to CSV
out_path = "/Users/rrworkspace/Downloads/TRBJ_genes.csv"
pd.DataFrame(filtered_rows, columns=["gene_name","sequence_nt","translation_aa","leftover_nt"]).to_csv(out_path, index=False)

# Print missing genes
missing_genes = [g for g in gene_names if g not in found_genes]
if missing_genes:
    print("Gene names not found in input file:", ", ".join(missing_genes))

print(f"Saved {len(filtered_rows)} records to {out_path}")
