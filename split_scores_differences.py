import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CONFIGURATION
input_file = "/fh/fast/hill_g/Rui/MHC2TCR_test_250722/analysis_results/compiled_scores_test/af3_all_scores.csv"
output_dir = "/fh/fast/hill_g/Rui/MHC2TCR_test_250722/analysis_results/compiled_scores_test/"
os.makedirs(output_dir, exist_ok=True)

# Load data
full_df = pd.read_csv(input_file)
full_df = full_df.set_index(["Clonotype", "Peptide"])

# Define peptide subsets
peptides1 = ["ayi", "ivn", "nya", "ptle", "tle"]
peptides2 = ["vsayi", "rrivn", "mnya", "pltle", "ltle"]

# Extract Clonotypes in the desired order from the first set
clonotypes_order = full_df.reset_index().query("Peptide in @peptides1")["Clonotype"].unique()

# Helper to construct heatmap matrix with fillna
def subset_matrix(df, peptides, clonotypes, metric):
    df_reset = df.reset_index()
    subset = df_reset[df_reset["Peptide"].isin(peptides) & df_reset["Clonotype"].isin(clonotypes)]
    matrix = subset.pivot(index="Clonotype", columns="Peptide", values=metric)
    matrix = matrix.reindex(index=clonotypes, columns=peptides)
    matrix = matrix.fillna(0)  # Fill missing values with 0
    return matrix

# Metrics to plot
metrics = ["mean_plddt", "iptm", "mean_pae", "interface_conf"]

for metric in metrics:
    heatmap1 = subset_matrix(full_df, peptides1, clonotypes_order, metric)
    heatmap2 = subset_matrix(full_df, peptides2, clonotypes_order, metric)

    # Save heatmap1
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap1, annot=True, fmt=".2f", cmap="Blues", cbar_kws={'label': metric})
    plt.title(f"Subset Heatmap 1: {metric}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"subset_heatmap1_{metric}.png"), dpi=300)
    plt.close()

    # Save heatmap2
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap2, annot=True, fmt=".2f", cmap="Greens", cbar_kws={'label': metric})
    plt.title(f"Subset Heatmap 2: {metric}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"subset_heatmap2_{metric}.png"), dpi=300)
    plt.close()

    # Difference heatmap
    diff = heatmap1 - heatmap2
    colors = diff.applymap(lambda x: 'lightblue' if x > 0 else ('white' if x == 0 else 'lightcoral'))
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(diff, annot=True, fmt=".2f", cbar=False, linewidths=.5, linecolor='gray', mask=diff.isna())
    for y in range(diff.shape[0]):
        for x in range(diff.shape[1]):
            if pd.notna(diff.iloc[y, x]):
                ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color=colors.iloc[y, x], alpha=0.5))
    plt.title(f"Difference Heatmap: {metric} (Set1 - Set2)")
    plt.xlabel("Peptide")
    plt.ylabel("Clonotype")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"difference_heatmap_{metric}.png"), dpi=300)
    plt.close()
