# TCR–pMHCII Interaction Screening via AF3

This repository contains code for modeling interactions between T cell receptors (TCRs) and MHC class II-peptide complexes using AlphaFold 3 (AF3).

### Features
- Batch processing of TCR–MHCII pairs
- Sequence input from JSON or FASTA
- Residue contact parsing and score extraction

### Requirements
- Python 3.8+
- AlphaFold 3 (access required)
- JAX, NumPy, Biopython, etc.

## WORKFLOW

### Generate Full-Length TCR Sequences from CDR3 CSV

This script constructs full-length TCR sequences using defined variable (TRAV/TRBV), joining (TRAJ/TRBJ), constant (TCRAC/TCRBC), and linker segments, along with custom CDR3α and CDR3β sequences.

**Input**

CSV file with the following format:

```csv
name,cdr3a,cdr3b
sample1,CAASGGSYIPTF,CASSLGQGTDTQYF
sample2,CAASRDNYGGKLTF,CASSIRSSYEQYF

Each row represents one TCR, with a unique name, the CDR3α sequence, and the CDR3β sequence.

**how to run**

Make sure to define your sequence components in the script:
```
TRAV = "TRAVSEQUENCE"
TRAJ = "TRAJSEQUENCE"
TCRAC = "TCRACSEQUENCE"
TRBV = "TRBVSEQUENCE"
TRBJ = "TRBJSEQUENCE"
TCRBC = "TCRBCSEQUENCE"
linker = "GGGGS"
```

run the script:
```
python generate_tcr_sequences_from_csv.py
```
**Output**

The output is written to full_tcr_sequences.txt, in FASTA-like format:
```
>sample1
TRAVSEQUENCECAASGGSYIPTFTRAJSEQUENCETCRACSEQUENCEGGGGSGGGGSGGGGSTRBVSEQUENCECASSLGQGTDTQYFTRBJSEQUENCETCRBCSEQUENCE
>sample2
TRAVSEQUENCECAASRDNYGGKLTFTRAJSEQUENCETCRACSEQUENCEGGGGSGGGGSGGGGSTRBVSEQUENCECASSIRSSYEQYFTRBJSEQUENCETCRBCSEQUENCE
```

