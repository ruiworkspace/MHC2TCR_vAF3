#!/net/software/containers/users/magnusb/local.sif
import warnings
warnings.filterwarnings("ignore", message=".*")
 
import json
import os
import sys
 
# Usage: python setup_af3_DLK1.py <DLK1_ECD_sequence> <Interactor_sequence>
dlk1_seq = sys.argv[1]  # DLK1 ECD sequence
interactor_seq = sys.argv[2]  # Interactor sequence
print("DLK1 ECD sequence:", dlk1_seq)
print("Interactor sequence:", interactor_seq)
 
# Remove zero-width space and whitespace from both sequences
dlk1_seq = dlk1_seq.replace('\u200b', '').strip()
interactor_seq = interactor_seq.replace('\u200b', '').strip()
 
# Set up both chains with no PTM modifications
# Chain A: DLK1 ECD, Chain B: Interactor
template = {
    'dialect': 'alphafold3',
    'version': 1,
    'name': 'DLK1_interaction',
    'sequences': [
        {'protein': {'id': 'A',
                     'sequence': dlk1_seq,
                     'modifications': [],
                     'unpairedMsa': '',
                     'pairedMsa': '',
                     'templates': [],
                     'unpairedMsaPath': ''}},
        {'protein': {'id': 'B',
                     'sequence': interactor_seq,
                     'modifications': [],
                     'unpairedMsa': '',
                     'pairedMsa': '',
                     'templates': [],
                     'unpairedMsaPath': ''}}
    ],
    'modelSeeds': [1]
}
 
os.makedirs('jsons', exist_ok=True)
json_path = os.path.join('jsons', 'DLK1_interaction.json')
 
with open(json_path, 'w') as f:
    json.dump(template, f, indent=4)
print(f"Wrote {json_path}")
 
# Optionally, you can add code to generate the af3_cmds file if needed
