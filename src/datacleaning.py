import os
import re

def ensure_dirs(*dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def load_script(script_path):
    with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def split_seasons(full_text, seasons_dir):
    season_split = full_text.split("SEASON 2", 1)
    season1_text = season_split[0].strip()
    season2_text = "SEASON 2" + season_split[1].strip()

    with open(os.path.join(seasons_dir, "season_1.txt"), "w", encoding="utf-8") as f:
        f.write(season1_text)
    with open(os.path.join(seasons_dir, "season_2.txt"), "w", encoding="utf-8") as f:
        f.write(season2_text)

    return season2_text

def split_episodes(season_text, episodes_dir):
    episode_splits = re.split(r"(EPISODE\s+\d+)", season_text)
    episode_splits = [e.strip() for e in episode_splits if e.strip()]

    episodes = {}
    for i in range(1, len(episode_splits), 2):
        ep_name = episode_splits[i]
        ep_text = episode_splits[i + 1] if i + 1 < len(episode_splits) else ""
        ep_num = re.search(r"\d+", ep_name).group(0)
        episodes[ep_num] = ep_text
        ep_filename = os.path.join(episodes_dir, f"episode_{ep_num}.txt")
        with open(ep_filename, "w", encoding="utf-8") as f:
            f.write(f"EPISODE {ep_num}\n{ep_text}")
    return episodes

def split_scenes(episodes, scenes_dir):
    for ep_num, ep_text in episodes.items():
        scene_pattern = r"(\[.*?\].*?)(?=\[|$)"
        scenes = re.findall(scene_pattern, ep_text, flags=re.DOTALL)
        for i, scene_text in enumerate(scenes, start=1):
            scene_filename = os.path.join(scenes_dir, f"episode_{ep_num}_scene_{i}.txt")
            with open(scene_filename, "w", encoding="utf-8") as f:
                f.write(scene_text.strip())

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), "../data")
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_output"))
    seasons_dir = os.path.join(output_dir, "seasons")
    episodes_dir = os.path.join(output_dir, "season_2_episodes")
    scenes_dir = os.path.join(output_dir, "season_2_scenes")

    ensure_dirs(output_dir, seasons_dir, episodes_dir, scenes_dir)

    script_path = os.path.join(base_dir, "DERRY-GIRLS-SCRIPT.txt")
    full_text = load_script(script_path)

    if "SEASON 2" not in full_text:
        raise ValueError("No 'SEASON 2' marker found in text.")

    season2_text = split_seasons(full_text, seasons_dir)
    episodes = split_episodes(season2_text, episodes_dir)
    split_scenes(episodes, scenes_dir)

    print("Seasons, episodes, and scenes saved.")

