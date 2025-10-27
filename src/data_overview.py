import os
import re
import csv
import matplotlib.pyplot as plt

def count_lines_and_speakers(scenes_dir):
    summary = []
    speaker_regex = re.compile(r"^([A-Z][A-Za-z\s]*):")  # Uppercase start, ends with colon
    
    for filename in sorted(os.listdir(scenes_dir)):
        if not filename.endswith(".txt"):
            continue
        file_path = os.path.join(scenes_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        num_lines = len(lines)
        speakers = set()
        for line in lines:
            match = speaker_regex.match(line)
            if match:
                speakers.add(match.group(1).strip())
        
        summary.append({
            "scene_file": filename,
            "num_lines": num_lines,
            "num_speakers": len(speakers)
        })
    return summary

def save_summary_csv(summary, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "scene_summary.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["scene_file", "num_lines", "num_speakers"])
        writer.writeheader()
        writer.writerows(summary)
    return csv_path

def plot_summary(summary, plots_dir):
    os.makedirs(plots_dir, exist_ok=True)

    scene_names = [s["scene_file"] for s in summary]
    num_lines = [s["num_lines"] for s in summary]
    num_speakers = [s["num_speakers"] for s in summary]

    x = range(len(scene_names))
    
    plt.figure(figsize=(15,6))
    
    plt.bar(x, num_lines, width=0.4, label="Lines", align="edge")
    plt.bar(x, num_speakers, width=-0.4, label="Speakers", align="edge")
    
    plt.xticks(x, scene_names, rotation=90)
    plt.ylabel("Count")
    plt.title("Lines and Speakers per Scene")
    plt.legend()
    plt.tight_layout()

    plot_path = os.path.join(plots_dir, "scene_summary.png")
    plt.savefig(plot_path)
    plt.close()
    return plot_path

if __name__ == "__main__":
    base_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_output"))
    scenes_dir = os.path.join(base_output_dir, "season_2_scenes")
    plots_dir = os.path.join(base_output_dir, "plots")

    summary = count_lines_and_speakers(scenes_dir)
    csv_path = save_summary_csv(summary, base_output_dir)
    plot_path = plot_summary(summary, plots_dir)

    print("CSV saved to:", csv_path)
    print("Plot saved to:", plot_path)
