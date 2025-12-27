import os
import re
import random
from collections import Counter

PRIMARY_CHARACTERS = ["Erin", "Mary", "Orla", "Gerry", "Michelle", "James", "Clare", "Sister Michael"]

def ensure_dirs(*dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def load_script(script_path):
    with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def split_seasons(full_text, seasons_dir):
    season_split = full_text.split("SEASON 2", 1)
    season1_text = season_split[0].strip()
    with open(os.path.join(seasons_dir, "season_1.txt"), "w", encoding="utf-8") as f:
        f.write(season1_text)
    return season1_text

def split_episodes(season_text):
    episode_splits = re.split(r"(EPISODE\s+\d+)", season_text)
    episode_splits = [e.strip() for e in episode_splits if e.strip()]
    episodes = {}
    for i in range(1, len(episode_splits), 2):
        ep_num = re.search(r"\d+", episode_splits[i]).group(0)
        episodes[ep_num] = episode_splits[i + 1]
    return episodes

def split_scenes(text):
    scene_pattern = r"(\[.*?\].*?)(?=\[|$)"
    return [s.strip() for s in re.findall(scene_pattern, text, flags=re.DOTALL)]

def detect_characters(scene, characters):
    return [c for c in characters if c in scene]

def character_statistics(episodes, characters=PRIMARY_CHARACTERS):
    all_scenes = []
    for ep_text in episodes.values():
        all_scenes.extend(split_scenes(ep_text))
    
    total_scenes = len(all_scenes)
    counter = Counter()

    for scene in all_scenes:
        scene_chars = detect_characters(scene, characters)
        counter.update(set(scene_chars))  # count each character only once per scene

    print(f"Total scenes: {total_scenes}\n")
    for char in characters:
        count = counter[char]
        pct = (count / total_scenes) * 100 if total_scenes > 0 else 0
        print(f"{char}: {count} scenes ({pct:.1f}%)")

def save_chunk_with_characters(episodes, output_path, max_tokens=1500):
    # Collect all scenes with their characters
    all_scenes = []
    for ep_text in episodes.values():
        for scene in split_scenes(ep_text):
            chars_in_scene = detect_characters(scene, PRIMARY_CHARACTERS)
            all_scenes.append((scene, chars_in_scene))

    # Ensure at least one scene per primary character
    selected_scenes = []
    used_scenes = set()
    for character in PRIMARY_CHARACTERS:
        for scene, chars in all_scenes:
            if character in chars and scene not in used_scenes:
                selected_scenes.append(scene)
                used_scenes.add(scene)
                break  # only one per character

    # Fill the rest randomly
    remaining_scenes = [s for s, _ in all_scenes if s not in used_scenes]
    random.shuffle(remaining_scenes)

    chunk_text = ""
    tokens = 0
    for scene in selected_scenes + remaining_scenes:
        scene_tokens = len(scene.split())
        if tokens + scene_tokens > max_tokens:
            break
        chunk_text += scene + "\n\n"
        tokens += scene_tokens

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(chunk_text.strip())

    print(f"Saved {tokens} tokens (~{len(chunk_text.split())} words) to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), "../data")
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_output"))
    seasons_dir = os.path.join(output_dir, "seasons")
    ensure_dirs(output_dir, seasons_dir)

    script_path = os.path.join(base_dir, "DERRY-GIRLS-SCRIPT.txt")
    full_text = load_script(script_path)

    season1_text = split_seasons(full_text, seasons_dir)
    episodes = split_episodes(season1_text)

    # Print character statistics
    character_statistics(episodes)

    # Save the chunk with all primary characters
    chunk_path = os.path.join(output_dir, "season1_chunk.txt")
    save_chunk_with_characters(episodes, chunk_path, max_tokens=1500)
