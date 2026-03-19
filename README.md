# Forensic LCM System

A Gradio-based forensic analysis application for scanning PDF documents, extracting statements, and generating contradiction-focused audit reports.

## Tech stack

- Python
- Gradio
- PDF/document processing modules in `modules/`
- Local HTML report generation in `outputs/`

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/orange-05/hybrid_2026.git
cd hybrid_2026
```

### 2. Create and activate a virtual environment

**Windows (Command Prompt):**

```bat
python -m venv env
env\Scripts\activate
```

**macOS / Linux / Git Bash:**

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
python app.py
```

By default, the Gradio app runs on `http://127.0.0.1:7860`.

## Netlify deployment

### Short answer

This project **cannot be deployed directly to Netlify in its current form**.

### Why Netlify is not a good fit

Netlify is best for:

- static sites
- frontend frameworks that build to static/server-rendered assets
- lightweight serverless functions

This repository is instead a **stateful Python/Gradio application** that:

- launches a long-running web server with `demo.launch(...)`
- loads document-processing and ML-style components at runtime
- handles uploaded PDF files and generates local output files

That architecture does **not** match Netlify's normal hosting model.

### Recommended deployment options

If you want this app online, use one of these instead:

1. **Hugging Face Spaces**
   - Best fit for Gradio apps.
   - Very little restructuring required.

2. **Render / Railway / Fly.io**
   - Good for Python web services.
   - Better if you want persistent app hosting.

3. **A VPS or cloud VM**
   - Best if you need full control over Python dependencies, storage, and runtime behavior.

## If you still want to use Netlify

You have two practical choices:

### Option A: Use Netlify only for a landing page

Host a static marketing/docs page on Netlify, and host the actual Python app somewhere else.

### Option B: Split the project into two parts

- **Frontend on Netlify**
- **Python API/backend on another host**

That would require a significant refactor:

- replace the Gradio UI with a separate frontend
- expose the forensic processing logic through an API
- move file processing/report generation to the backend host

## Suggested next step

If your goal is the fastest deployment with the fewest code changes, deploy this repo to **Hugging Face Spaces** or **Render** instead of Netlify.
