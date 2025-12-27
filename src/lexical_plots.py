import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Paths
# -----------------------------
SUMMARY_PATH = "../data_output/lexical_analysis/lexical_summary.csv"
ANALYSIS_PATH = "../data_output/lexical_analysis/lexical_analysis.csv"
OUTPUT_DIR = "../data_output/lexical_analysis/plots"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Load the summary CSV
# -----------------------------
df = pd.read_csv(SUMMARY_PATH)

# Only keep human and LLM rows
df = df[df["Unnamed: 0"].str.contains("human|LLM")].copy()

# Clean metric names
df["text_type"] = df["Unnamed: 0"].apply(lambda x: "Human" if "human" in x else "LLM")
df["metric"] = df["Unnamed: 0"].apply(lambda x: x.replace("human_scene_", "")
                                              .replace("LLM_scene_", ""))

df = df.drop(columns=["Unnamed: 0"])

# -----------------------------
# Plotting function for summary stats
# -----------------------------
def make_density_plot(metric_name, mean_h, sd_h, mean_l, sd_l):
    plt.figure(figsize=(8, 5))

    # Create smooth density lines manually
    sns.kdeplot(
        pd.Series([mean_h - sd_h, mean_h, mean_h + sd_h]),
        label=f"Human (Mean={mean_h:.2f}, SD={sd_h:.2f})",
        linestyle="--"
    )
    sns.kdeplot(
        pd.Series([mean_l - sd_l, mean_l, mean_l + sd_l]),
        label=f"LLM (Mean={mean_l:.2f}, SD={sd_l:.2f})",
        linestyle="-"
    )

    plt.title(f"Density Plot (Summary): {metric_name}")
    plt.xlabel(metric_name)
    plt.ylabel("Density")
    plt.legend()

    out_path = os.path.join(OUTPUT_DIR, f"{metric_name}_density_summary.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

# -----------------------------
# Generate plots for each metric (summary)
# -----------------------------
print("Generating summary density plots...")
for metric in df["metric"].unique():
    row_h = df[(df["metric"] == metric) & (df["text_type"] == "Human")].iloc[0]
    row_l = df[(df["metric"] == metric) & (df["text_type"] == "LLM")].iloc[0]

    mean_h, sd_h = row_h["Mean"], row_h["SD"]
    mean_l, sd_l = row_l["Mean"], row_l["SD"]

    make_density_plot(metric, mean_h, sd_h, mean_l, sd_l)

print("\n✓ All summary density plots saved!")

# -----------------------------
# Load lexical_analysis.csv for per-row plotting
# -----------------------------
print("\nGenerating per-row density plots...")
lex_df = pd.read_csv(ANALYSIS_PATH)

# Define metrics to plot
metrics = ["MTLD", "CTTR", "TTR", "avg_sentence_length", "sentence_count", "word_count"]

# -----------------------------
# Plotting function for per-row data (connected scatter plot with row number on y-axis)
# -----------------------------
def make_per_row_scatter_plot(metric_name, df_subset):
    plt.figure(figsize=(10, 8))
    
    # Reset index to get row numbers
    df_subset = df_subset.reset_index(drop=True)
    n_rows = len(df_subset)
    
    # Plot each row as a line connecting Human to LLM
    for idx in range(n_rows):
        human_val = df_subset.loc[idx, 'human_value']
        llm_val = df_subset.loc[idx, 'llm_value']
        
        # Plot line connecting the two points (horizontal line at row idx) - BLACK
        plt.plot([human_val, llm_val], [idx, idx], 
                color='black', alpha=0.5, linewidth=1.5)
        
        # Plot points - Human in blue, LLM in red
        plt.scatter([human_val], [idx], color='blue', s=50, alpha=0.8, zorder=3)
        plt.scatter([llm_val], [idx], color='red', s=50, alpha=0.8, zorder=3)
    
    # Customize plot
    plt.xlabel(metric_name)
    plt.ylabel('Scene Number')
    plt.title(f"Per-Row Comparison: {metric_name}\n(Each line connects Human (blue) → LLM (red) for the same scene)")
    plt.grid(True, alpha=0.3, axis='x')
    
    # Add mean lines (vertical now since we flipped axes)
    mean_human = df_subset['human_value'].mean()
    mean_llm = df_subset['llm_value'].mean()
    sd_human = df_subset['human_value'].std()
    sd_llm = df_subset['llm_value'].std()
    
    plt.axvline(x=mean_human, color='blue', linestyle='--', alpha=0.5, 
                linewidth=2, label=f'Human (M={mean_human:.2f}, SD={sd_human:.2f})')
    plt.axvline(x=mean_llm, color='red', linestyle='--', alpha=0.5, 
                linewidth=2, label=f'LLM (M={mean_llm:.2f}, SD={sd_llm:.2f})')
    
    plt.legend(loc='best')
    plt.tight_layout()
    
    out_path = os.path.join(OUTPUT_DIR, f"{metric_name}_scatter_perrow.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

# -----------------------------
# Generate per-row plots for each metric
# -----------------------------
import numpy as np

for metric in metrics:
    human_col = f"human_scene_{metric}"
    llm_col = f"LLM_scene_{metric}"
    
    # Check if columns exist
    if human_col in lex_df.columns and llm_col in lex_df.columns:
        # Create a subset dataframe with both columns
        df_subset = lex_df[[human_col, llm_col]].copy()
        df_subset.columns = ['human_value', 'llm_value']
        
        # Remove rows with NaN in either column
        df_subset = df_subset.dropna()
        
        if len(df_subset) > 0:
            make_per_row_scatter_plot(metric, df_subset)
        else:
            print(f"Warning: No valid data for {metric}")
    else:
        print(f"Warning: Columns not found for {metric}")

print("\n✓ All per-row density plots saved!")
print(f"\nAll plots saved to: {OUTPUT_DIR}")