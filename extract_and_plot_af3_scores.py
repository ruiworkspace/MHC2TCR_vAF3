#!/usr/bin/env python3

import os
import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Configuration ===
results_dir = "/fh/fast/hill_g/Rui/MHC2TCR_test_250722/test_output"   
output_dir  = "/fh/fast/hill_g/Rui/MHC2TCR_test_250722/analysis_results/compiled_scores"
os.makedirs(output_dir, exist_ok=True)

# === Score Extraction Function ===
def extract_scores(summary_path, full_data_path):
    scores = {}
    try:
        with open(summary_path, "r") as f:
            summary = json.load(f)
        with open(full_data_path, "r") as f:
            full_data = json.load(f)

        # iPTM score
        if summary.get("chain_pair_iptm") and summary["chain_pair_iptm"][0]:
            scores['iptm'] = summary["chain_pair_iptm"][0][0]
        elif summary.get("chain_ptm"):
            scores['iptm'] = summary["chain_ptm"][0]

        # Mean pLDDT
        if "atom_plddts" in full_data:
            scores['mean_plddt']  = sum(full_data["atom_plddts"]) / len(full_data["atom_plddts"])

        # Mean PAE
        if "pae" in full_data:
            pae_matrix = full_data["pae"]
            scores['mean_pae']    = sum(sum(row) / len(row) for row in pae_matrix) / len(pae_matrix)

        # Interface confidence
        if "contact_probs" in full_data:
            contact_probs = full_data["contact_probs"]
            # average over all entries
            scores['interface_conf'] = sum(map(sum, contact_probs)) / (len(contact_probs) * len(contact_probs[0]))

    except Exception as e:
        print(f"⚠️ Error reading {summary_path} or {full_data_path}: {e}")

    return scores

# === Gather All JSON Pairs ===
# Expect filenames like:
#   sample0_clonotype5__ltle_summary_confidences.json
#   sample0_clonotype5__ltle_confidences.json

pattern = re.compile(
    r'^(?P<sample>sample0)_clonotype(?P<clono>\d+)__(?P<peptide>[^_]+)_(?P<type>summary_confidences|confidences)\.json$'
)

file_pairs = {}

for root, _, files in os.walk(results_dir):
    for fname in files:
        if not fname.endswith(".json"):
            continue
        m = pattern.match(fname)
        if not m:
            continue

        clonotype = int(m.group("clono"))
        peptide   = m.group("peptide")
        ftype     = m.group("type")  # summary_confidences or confidences

        key = (f"clonotype{clonotype}", peptide)
        file_pairs.setdefault(key, {})[ftype] = os.path.join(root, fname)

# keep only those with both files
file_pairs = {
    key: (paths["summary_confidences"], paths["confidences"])
    for key, paths in file_pairs.items()
    if "summary_confidences" in paths and "confidences" in paths
}

print(f"✔ Found {len(file_pairs)} clonotype–peptide pairs to process\n")

# === Extract and Organize Scores ===

compiled_scores = {}  # { (clonotype, peptide) : score_dict }

for (clono, peptide), (sum_p, full_p) in file_pairs.items():
    scores = extract_scores(sum_p, full_p)
    if scores:
        compiled_scores.setdefault((clono, peptide), scores)

if not compiled_scores:
    raise RuntimeError("No scores extracted; check that your JSON files match the expected format/naming.")

# Build a DataFrame with MultiIndex (Clonotype, Peptide)
rows = []
for (clono, peptide), scores in compiled_scores.items():
    row = {"Clonotype": clono, "Peptide": peptide}
    row.update(scores)
    rows.append(row)

df = pd.DataFrame(rows).set_index(["Clonotype", "Peptide"])
csv_path = os.path.join(output_dir, "af3_all_scores.csv")
df.to_csv(csv_path)
print(f"✔ Saved all scores to CSV: {csv_path}\n")

# === Plot Heatmaps ===

for metric in ["mean_plddt", "iptm", "mean_pae", "interface_conf"]:
    if metric not in df.columns:
        print(f"• Metric '{metric}' not found—skipping heatmap.")
        continue

    heat_df = df.unstack(level="Peptide")[metric]
    plt.figure(figsize=(10, 8))
    sns.heatmap(heat_df, annot=True, fmt=".2f", cmap="viridis", cbar_kws={"label": metric})
    plt.title(f"AF3: {metric} by TCR (clonotype) × Peptide")
    plt.xlabel("Peptide")
    plt.ylabel("Clonotype")
    plt.tight_layout()

    png = os.path.join(output_dir, f"af3_{metric}_heatmap.png")
    pdf = os.path.join(output_dir, f"af3_{metric}_heatmap.pdf")
    plt.savefig(png, dpi=300)
    plt.savefig(pdf)
    plt.close()

    print(f"✔ Saved heatmap '{metric}':\n    {png}\n    {pdf}\n")

print("All done!") 
