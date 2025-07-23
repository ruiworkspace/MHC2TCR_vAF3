import json
import sys
import os
from pathlib import Path
from Bio import SeqIO

# Input arguments
filepath = sys.argv[1]      # Text file listing PDB paths
target_seq = sys.argv[2]    # Peptide sequence with (PTR)

# Determine PTM position
ptm_pos = target_seq.find('(PTR)')
if ptm_pos == -1:
    raise ValueError("The PTM '(PTR)' was not found in the target sequence.")
ptm_pos += 1  # Convert to 1-indexed

# Replace modified residue for AF3 input sequence
clean_seq = target_seq.replace('(PTR)', 'Y')

# JSON template
template = {
    'dialect': 'alphafold3',
    'version': 1,
    'name': 'template',
    'sequences': [
        {'protein': {'id': 'A', 'sequence': '', 'modifications': [], 'unpairedMsa': '', 'pairedMsa': '', 'templates': [], 'unpairedMsaPath': ''}},
        {'protein': {'id': 'B', 'sequence': clean_seq, 'modifications': [{'ptmType': 'PTR', 'ptmPosition': ptm_pos}], 'unpairedMsa': '', 'pairedMsa': '', 'templates': [], 'unpairedMsaPath': ''}}
    ],
    'modelSeeds': [1]
}

# Output folder
os.makedirs('jsons', exist_ok=True)

# Process each PDB file
with open(filepath) as f:
    for line in f:
        pdb_path = line.strip()
        if not pdb_path:
            continue

        try:
            with open(pdb_path, 'r') as pdb_file:
                for record in SeqIO.parse(pdb_file, 'pdb-atom'):
                    if record.id.endswith('A'):
                        seq_a = str(record.seq).replace('X', 'Y')
                        break
                else:
                    raise ValueError("No chain ending with 'A' found.")

            # Prepare JSON
            json_data = template.copy()
            json_data['sequences'][0]['protein']['sequence'] = seq_a
            json_data['name'] = Path(pdb_path).stem

            # Write JSON
            json_path = Path(f"./jsons/{Path(pdb_path).stem}.json")
            with open(json_path, 'w') as jf:
                json.dump(json_data, jf, indent=4)

        except Exception as e:
            print(f"Error processing {pdb_path}: {e}")
