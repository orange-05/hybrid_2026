# Forensic LCM System

This repository now supports two use cases:

- a **static Netlify deployment** from the `public/` folder for your live site
- the original **local Python/Gradio forensic scanner** for full PDF analysis

## Netlify dashboard values

Use these values in **Project configuration → Build & deploy → Build settings**:

```text
Base directory: public
Package directory: leave empty
Build command: echo "Static site ready"
Publish directory: .
Functions directory: leave empty
```

## Netlify CLI commands

```bash
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --dir=public
netlify deploy --prod --dir=public
```

## Run locally

### Windows Command Prompt

```bat
git clone https://github.com/orange-05/hybrid_2026.git
cd hybrid_2026
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS / Linux / Git Bash

```bash
git clone https://github.com/orange-05/hybrid_2026.git
cd hybrid_2026
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

The Gradio app starts at `http://127.0.0.1:7860` and performs the full forensic scan locally.

## Project structure

- `public/` contains the static Netlify-ready site.
- `app.py` and `modules/` contain the Python/Gradio forensic analysis application.
- `outputs/` is created locally when forensic reports are generated.
