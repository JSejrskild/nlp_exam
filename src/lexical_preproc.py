import pandas as pd
import os

# -------------------------
# Paths
# -------------------------
gpt_overview_path = "../data_output/GPT_scenes/GPT_scene_overview.csv"
gpt5_scenes_path = "../data_output/GPT5_scenes.csv"
human_folder = "../data_output/data_selected"
output_path = "../data_output/lexical_analysis/overview.csv"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

# -------------------------
# Load GPT overview
# -------------------------
gpt_overview = pd.read_csv(gpt_overview_path)

# Ensure filenames have .txt
gpt_overview["filename"] = gpt_overview["filename"].astype(str)
gpt_overview["filename"] = gpt_overview["filename"].apply(
    lambda x: x if x.endswith(".txt") else f"{x}.txt"
)

# Normalize to lowercase for merging
gpt_overview["filename"] = gpt_overview["filename"].str.lower()

# -------------------------
# Load GPT5 scenes
# -------------------------
gpt5_scenes = pd.read_csv(gpt5_scenes_path)
gpt5_scenes = gpt5_scenes.rename(columns={"scene": "LLM_scene"})

# -------------------------
# Load human scenes (only matching filenames)
# -------------------------
needed_files = set(gpt_overview["filename"])

human_data = []
for fname in os.listdir(human_folder):
    fname_lower = fname.lower()
    if fname_lower in needed_files:
        with open(os.path.join(human_folder, fname), "r", encoding="utf-8") as f:
            human_data.append({"filename": fname_lower, "human_scene": f.read()})

human_df = pd.DataFrame(human_data)

# -------------------------
# Combine all data
# -------------------------
# Start with GPT overview
combined_df = gpt_overview.copy()

# Append GPT5 summaries & LLM_scene by row order
combined_df["summary"] = gpt5_scenes["summary"]
combined_df["LLM_scene"] = gpt5_scenes["LLM_scene"]

# Merge human scenes by filename
combined_df = combined_df.merge(human_df, on="filename", how="left")

# -------------------------
# Save output
# -------------------------
combined_df.to_csv(output_path, index=False)

print("Saved:", output_path)
print("Missing human scenes:", combined_df["human_scene"].isna().sum())
