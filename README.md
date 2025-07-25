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

### 1. Generate Full-Length TCR Sequences from CDR3 CSV

This script constructs full-length TCR sequences using defined variable (TRAV/TRBV), joining (TRAJ/TRBJ), constant (TCRAC/TCRBC), and linker segments, along with custom CDR3α and CDR3β sequences.

**a.Input**

CSV file with the following format:

```csv
name,cdr3a,cdr3b
sample1,CAASGGSYIPTF,CASSLGQGTDTQYF
sample2,CAASRDNYGGKLTF,CASSIRSSYEQYF
```

Each row represents one TCR, with a unique name, the CDR3α sequence, and the CDR3β sequence.


**b.How to Run**

Make sure to define your sequence components in the script:

```python
TRAV = "TRAVSEQUENCE"
TRAJ = "TRAJSEQUENCE"
TCRAC = "TCRACSEQUENCE"
TRBV = "TRBVSEQUENCE"
TRBJ = "TRBJSEQUENCE"
TCRBC = "TCRBCSEQUENCE"
linker = "GGGGS"
```


run the script:

```bash
python generate_tcr_sequences_from_csv.py
```

**c.Output**

The output is written to full_tcr_sequences.txt, in FASTA-like format:

```
>sample1
TRAVSEQUENCECAASGGSYIPTFTRAJSEQUENCETCRACSEQUENCEGGGGSGGGGSGGGGSTRBVSEQUENCECASSLGQGTDTQYFTRBJSEQUENCETCRBCSEQUENCE
>sample2
TRAVSEQUENCECAASRDNYGGKLTFTRAJSEQUENCETCRACSEQUENCEGGGGSGGGGSGGGGSTRBVSEQUENCECASSIRSSYEQYFTRBJSEQUENCETCRBCSEQUENCE
```

### 2. Using AF3 on the Computing Cluster 

**this part refers to Albert's fork**


- In log-in computing node, create an "input" and "output" directory
- In the "input" directory, upload the jsons file
  - You can put multiple jobs into a single JSON file by adding a comma after the last "}" and putting another block like this one (ie several blocks like this separated by commas and between the first "[" and the last "]".
  - Or just put multiple JSON files in the inputs folder. This "server" JSON format is described here: https://github.com/google-deepmind/alphafold/tree/main/server There is a newer format that you can also use, see here: https://github.com/google-deepmind/alphafold3/blob/main/docs/input.md
- Next, upload and the file "af3run.sh" in this repository.
  - Edit the following line in "af3run.sh":
```
export OUTPUT_DIR="YOUR OUTPUT FOLDER DIRECTORY HERE"
export INPUT_DIR="YOUR INPUT FOLDER DIRECTORY HERE"
```
- Now, you're ready to submit the job as follows in the directory of "af3run.sh" shell script:
```
sbatch af3run.sh
```
- Check the output slurm file for error messages; otherwise the final output should be accessible in the "OUTPUT_DIR" that was specified above.
