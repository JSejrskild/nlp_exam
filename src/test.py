import pandas as pd
import os

df_check = pd.read_csv("JohanneSejrskildRejsenhus#9686/nlp_exam/data_output/scene_summary.csv")
print("Rows in written CSV:", len(df_check))

txt_files = [f for f in os.listdir("JohanneSejrskildRejsenhus#9686/nlp_exam/data_output/season_2_scenes") if f.endswith(".txt")]
print(f"Found {len(txt_files)} .txt files in {"JohanneSejrskildRejsenhus#9686/nlp_exam/data_output/season_2_scenes"}")


# Path to your CSV file
csv_path = os.path.join("JohanneSejrskildRejsenhus#9686/nlp_exam", "data_output", "scene_summary.csv")

# Load the data
df = pd.read_csv(csv_path)

# Filter for episode 4 scene 10
scene_name = "episode_4_scene_10.txt"
scene_info = df[df["scene_file"] == scene_name]

if not scene_info.empty:
    num_lines = scene_info["num_lines"].iloc[0]
    print(f"{scene_name} has {num_lines} lines.")
else:
    print(f"{scene_name} not found in CSV.")
