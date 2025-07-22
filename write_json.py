import json

# Define your sequences as a dictionary
# You can use any identifier as the key
sequences = {
    "seq1": "MKTFFVLVLLPLVSSQCVNLTTRT",
    "seq2": "GAVLILALLTLVQLQSPALGNSS",
    "seq3": "MGLSDGEWQLVLNVWGKVEADIP",
}

# Write the sequences to a JSON file
with open("amino_acid_sequences.json", "w") as f:
    json.dump(sequences, f, indent=4)

print("Sequences written to amino_acid_sequences.json")
