import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Paths
base = "JohanneSejrskildRejsenhus#9686/nlp_exam/data_output"
gpt_file = os.path.join(base, "GPT5_scenes.csv")
non_gpt_folder = os.path.join(base, "data_selected")
output_folder = os.path.join(base, "GPT_scenes")
overview_file = os.path.join(output_folder, "GPT_scene_overview.csv")

os.makedirs(output_folder, exist_ok=True)


def clean_and_extract(scene_text):
    """Clean GPT scene text: remove line numbers and keep scene instructions."""
    lines = scene_text.split("\n")
    output = []

    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            continue
        # remove line numbers at the start
        stripped = re.sub(r"^\s*\d+\s*[\.\:\)\-]\s*", "", stripped)
        output.append(stripped)

    return output


def process_scenes(gpt_file, non_gpt_folder, output_folder, overview_file):
    """Process GPT scenes into individual txt files and create an overview CSV."""
    df = pd.read_csv(gpt_file)
    original_files = sorted([f for f in os.listdir(non_gpt_folder) if f.endswith(".txt")])

    if len(original_files) != len(df):
        print("Warning: number of GPT scenes and original files do not match!")

    overview_rows = []

    for idx, row in df.iterrows():
        scene_text = row["scene"]
        summary = row["summary"]

        cleaned_lines = clean_and_extract(scene_text)

        filename = original_files[idx]
        output_path = os.path.join(output_folder, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            for line in cleaned_lines:
                f.write(line + "\n")
                f.write("\n")  # blank line between each line

        overview_rows.append({
            "scene_number": idx + 1,
            "filename": filename,
            "summary": summary,
            "num_lines_after_cleaning": len(cleaned_lines),
            "num_lines_original": row["num_lines"],
        })

    pd.DataFrame(overview_rows).to_csv(overview_file, index=False)
    print(f"Processed {len(df)} scenes and saved overview to {overview_file}")


def plot_line_counts(overview_file, output_folder):
    """Plot number of lines in original vs GPT cleaned scenes."""
    df = pd.read_csv(overview_file)

    scenes = df["scene_number"]
    original = df["num_lines_original"]
    cleaned = df["num_lines_after_cleaning"]

    plt.figure(figsize=(14, 6))
    plt.plot(scenes, original, marker="o", label="Original number of lines")
    plt.plot(scenes, cleaned, marker="o", label="GPT cleaned number of lines")

    plt.title("Number of Lines Per Scene: Original vs GPT cleaned")
    plt.xlabel("Scene number")
    plt.ylabel("Number of lines")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    plot_path = os.path.join(output_folder, "diff_length.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved to {plot_path}")


# ------------------ Run ------------------
process_scenes(gpt_file, non_gpt_folder, output_folder, overview_file)
plot_line_counts(overview_file, output_folder)
