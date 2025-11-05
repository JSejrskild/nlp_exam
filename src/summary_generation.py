import os
import re
import pandas as pd
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, pipeline

def summarize_with_pegasus():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    scenes_dir = os.path.join(base_dir, "data_output", "data_selected")
    summaries_dir = os.path.join(base_dir, "data_output", "summaries_pegasus")
    os.makedirs(summaries_dir, exist_ok=True)

    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    def summarize_text(text):
        tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
        summary_ids = model.generate(**tokens)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def extract_episode_scene(filename):
        match = re.match(r"episode_(\d+)_scene_(\d+)\.txt", filename)
        if match:
            return match.groups()
        return None, None

    records = []

    for filename in sorted(os.listdir(scenes_dir)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(scenes_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        num_lines = len([line for line in text.splitlines() if line.strip()])
        summary = summarize_text(text)

        episode, scene = extract_episode_scene(filename)
        if episode and scene:
            summary_file = os.path.join(summaries_dir, f"summary_episode_{episode}_scene_{scene}.txt")
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(summary)

        records.append({
            "scene_file": filename,
            "num_lines": num_lines,
            "summary": summary
        })

    df_summaries = pd.DataFrame(records)
    csv_path = os.path.join(summaries_dir, "scene_summaries.csv")
    df_summaries.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved Pegasus summaries CSV to {csv_path}")


def summarize_with_BART(test_n=5):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    scenes_dir = os.path.join(base_dir, "data_output", "data_selected")
    summaries_dir = os.path.join(base_dir, "data_output", "summaries_BART")
    os.makedirs(summaries_dir, exist_ok=True)

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def extract_episode_scene(filename):
        match = re.match(r"episode_(\d+)_scene_(\d+)\.txt", filename)
        if match:
            return match.groups()
        return None, None

    records = []
    count = 0

    for filename in sorted(os.listdir(scenes_dir)):
        if count >= test_n:
            break
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(scenes_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        num_lines = len([line for line in text.splitlines() if line.strip()])
        print(f"Processing {filename} ({num_lines} lines)")
        summary_output = summarizer(text, max_length=200, min_length=30, do_sample=False)
        summary = summary_output[0]["summary_text"]

        episode, scene = extract_episode_scene(filename)
        if episode and scene:
            summary_filename = f"summary_episode_{episode}_scene_{scene}.txt"
        else:
            summary_filename = f"summary_{filename}"
        summary_path = os.path.join(summaries_dir, summary_filename)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        records.append({
            "scene_file": filename,
            "num_lines": num_lines,
            "summary": summary
        })
        count += 1

    df = pd.DataFrame(records)
    csv_path = os.path.join(summaries_dir, "scene_summaries_BART.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print("Saved BART summaries CSV to:", csv_path)
    print("Individual summary files saved in:", summaries_dir)


from transformers import pipeline

def summarize_with_meeting_model(test_n=5):
    """
    Summarize a limited number of scene files using the dialogue/meeting summarization model.
    Saves each summary as a .txt and collects all in a CSV.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    scenes_dir = os.path.join(base_dir, "data_output", "data_selected")
    summaries_dir = os.path.join(base_dir, "data_output", "summaries_MEETING")
    os.makedirs(summaries_dir, exist_ok=True)

    # Load the meeting summarization pipeline
    summarizer = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")

    def extract_episode_scene(filename):
        match = re.match(r"episode_(\d+)_scene_(\d+)\.txt", filename)
        if match:
            return match.groups()
        return None, None

    records = []
    count = 0

    for filename in sorted(os.listdir(scenes_dir)):
        if count >= test_n:
            break
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(scenes_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        num_lines = len([line for line in text.splitlines() if line.strip()])
        print(f"Processing {filename} ({num_lines} lines)")

        # Generate summary
        summary_output = summarizer(text, max_length=200, min_length=30, do_sample=False)
        summary = summary_output[0]["summary_text"]

        # Save individual summary file
        episode, scene = extract_episode_scene(filename)
        if episode and scene:
            summary_filename = f"summary_episode_{episode}_scene_{scene}.txt"
        else:
            summary_filename = f"summary_{filename}"
        summary_path = os.path.join(summaries_dir, summary_filename)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        # Record for CSV
        records.append({
            "scene_file": filename,
            "num_lines": num_lines,
            "summary": summary
        })
        count += 1

    # Save CSV of all summaries
    df = pd.DataFrame(records)
    csv_path = os.path.join(summaries_dir, "scene_summaries_MEETING.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")

    print("Saved MEETING model summaries CSV to:", csv_path)
    print("Individual summary files saved in:", summaries_dir)


if __name__ == "__main__":
    
    # summarize_with_pegasus()
    #summarize_with_BART(test_n=5)
    summarize_with_meeting_model(test_n = 110)
