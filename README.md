# NLP exam - Authorship Concealed: Reader Preferences for Human- and LLM-Generated Television Scenes

## Project Description
This project investigates whether large language models (LLMs) can generate TV-series scenes that are detectable as AI-generated or preferred over human written scenes in a human evaluation experiment.

The pipeline includes:
- Splitting TV-series transcripts into scenes
- Generating new scenes using a pre-defined prompt + summary
- Preparing experimental material for human participant evaluation
- Analyzing detectability and preference data collected from human experiments

The goal is to contribute to the debate on AI and creativity in narrative generation and its implications for industries such as film and TV.

# Repository Structure
```{txt}
nlp_exam/
─ data/
│   ├── DERRY-GIRLS-SCRIPT.txt
│   ├── Manuscript-study-full-data.csv
│   └── Manuscript-study-incremental-data.csv
├── data_output/
│   ├── GPT_scenes/
│   │   ├── GPT_scene_overview.csv
│   │   ├── diff_length.png
│   │   ├── episode_1_scene_12.txt
│   │   ├── ...
│   │   └── episode_6_scene_9.txt
│   ├── data_selected/
│   │   ├── episode_1_scene_12.txt
│   │   ├── ...
│   │   └── episode_6_scene_9.txt
│   ├── lexical_analysis/
│   │   ├── lexical_analysis.csv
│   │   ├── lexical_summary.csv
│   │   ├── overview.csv
│   │   └── plots/
│   │       └── scene_summary.png
│   ├── season_2_episodes/
│   │   ├── episode_1.txt
│   │   ├── ...
│   │   └── episode_6.txt
│   ├── season_2_scenes/
│   │   ├── episode_1_scene_1.txt
│   │   ├── ...
│   │   └── episode_6_scene_22.txt
│   ├── seasons/
│   │   ├── season_1.txt
│   │   └── season_2.txt
│   ├── summaries_BART/
│   │   ├── scene_summaries_BART.csv
│   │   ├── summary_episode_1_scene_12.txt
│   │   ├── ...
│   │   └── summary_episode_last.txt
│   ├── summaries_MEETING/
│   │   ├── scene_summaries_MEETING.csv
│   │   ├── summary_episode_1_scene_12.txt
│   │   ├── ...
│   │   └── summary_episode_last.txt
│   └── summaries_pegasus/
│       ├── scene_summary.csv
│       ├── summary_episode_1_scene_12.txt
│       ├── ...
│       └── GPT5_scenes.csv
├── src/
│   ├── beh_analysis_files/
│   │   └── figure-latex/
│   ├── GPT_datacleaning.py
│   ├── GPT_prompting_API.ipynb
│   ├── baseline_info.py
│   ├── beh_analysis.Rmd
│   ├── data_overview.py
│   ├── data_selection.py
│   ├── datacleaning.py
│   ├── lexical_analysis.py
│   ├── lexical_plots.py
│   ├── lexical_preproc.py
│   └── summary_generation.py
├── .gitignore
├── README.md
├── archive.zip
├── github_setup.sh
└── requirements.txt

    
# Installation

### Clone the repository:

git clone https://github.com/JSejrskild/nlp_exam.git

cd nlp_exam

### Set up a Python environment (optional but recommended):

python -m venv env
source env/bin/activate (On Windows: env\Scripts\activate)

### Install required packages:

pip install -r requirements.txt

# Usage
All code is run from /nlp_exam

## Generate manuscripts
*For some of these steps you need an API key. You should therefore have a key.txt file at the nlp_exam level with your API key that begins with sk-proj-*
Run the following files:

datacleaning.py
data_selection.py
summary_generation.py
GPT_prompting_API.ipynb
GPT_datacleaning.py

## Compute Lexical meassures
Run the following files:

lexical_preproc.py
lexical_analysis.py
lexical_plots.py

## Run analysis
Run the following file:

beh_analysis.Rmd


# Counsel Chat Copyright notice
MIT License

Copyright (c) 2020 nbertagnolli

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

