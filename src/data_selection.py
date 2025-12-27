import os
import shutil
import pandas as pd

# Information from scenes are in data_output/scene_summary.csv
# Scene length more between 15-30
# Speakers more than one
# Selected scenes copied into folder data_output/data_selected. 
# The scenes are located in /data_output/season_2_scenes and are named as they are in the scene_summary column "scene_file"

def main():
    # Load data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    scene_summary_path = os.path.join(base_dir, "data_output", "scene_summary.csv")

    print("Loading scene summary from:", scene_summary_path)
    df = pd.read_csv(scene_summary_path)
    # Filter scenes
    filtered_df = df[(df["num_lines"].between(15, 30)) & (df["num_speakers"] > 1)]
    print(f"Selected {len(filtered_df)} scenes matching criteria.")

    # Copy selected scenes
    src_dir = os.path.join(base_dir, "data_output", "season_2_scenes")
    dst_dir = os.path.join(base_dir, "data_output", "data_selected")
    os.makedirs(dst_dir, exist_ok=True)

    for scene_file in filtered_df["scene_file"]:
        src_path = os.path.join(src_dir, scene_file)
        dst_path = os.path.join(dst_dir, scene_file)

        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
        else:
            print(f"Warning: Scene file not found: {scene_file}")

    print("Scene selection complete.")
    print(f"Copied {len(os.listdir(dst_dir))} files to {dst_dir}.")



if __name__ == "__main__":
    main()


