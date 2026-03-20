# Forensic LCM System

A forensic analysis project that now supports **two use cases**:

- a **static Netlify deployment** from the `public/` folder for your live site
- the original **local Python/Gradio forensic scanner** for full PDF analysis

## Tech stack

- Python
- Gradio
- PDF/document processing modules in `modules/`
- Local HTML report generation in `outputs/`
- Static frontend assets in `public/`

## Netlify dashboard values

Use these values in **Project configuration → Build & deploy → Build settings**:

```text
Base directory: leave empty
Package directory: leave empty
Build command: echo "Static site ready"
Publish directory: public
Functions directory: leave empty