# Forensic LCM-LLM — Project Requirements Document

> **Purpose**: Personal reference for shipping / migrating this project to another system or team.  
> **Last updated**: September 2026  
> **Status**: Production-qualified (85 pytest tests pass, Docker-ready)

---

## 1. Project Summary

**Forensic LCM-LLM** is a hybrid Large Consulting Model — Large Language Architecture for **agentic financial forensics**. It ingests PDF financial documents (SEC filings, annual reports, IPO prospectuses, audit reports) and detects contradictions across four modalities: semantic, numeric, intent, and ratio.

**Core value proposition**: Cross-page financial figure mismatch detection + management narrative vs. reality gap analysis, with human-in-the-loop annotation to prune false positives (142 → 3 FP).

---

## 2. Functional Requirements

### 2.1 Document Ingestion
- Accept multi-page PDFs (tested up to 422 pages)
- Extract text and tables from all pages
- Handle SEC filings (10-K, 20-F), IPO DRHP/RHP, bank audit reports
- Sentence-level segmentation with WtPSplitter (canine-medium)

### 2.2 Contradiction Detection (4 Modalities)
| Modality | Technique | Output |
|----------|-----------|--------|
| Semantic | Hierarchical LCM + cosine similarity on sentence embeddings | Typed contradictions (11 types) |
| Numeric | Figure extraction, cross-page metric mapping, variance analysis | Numeric mismatches with % difference |
| Intent | Keyword-based intent classification (strategic positive vs operational negative) | Narrative vs reality gaps |
| Ratio | Cross-page ratio computation (PAT/revenue, debt/equity, etc.) | Ratio drift alerts |

### 2.3 Risk Scoring
- Severity-weighted algorithm (CRITICAL=25, HIGH=15, MEDIUM=8, LOW=3)
- Score 0–100, calibrated against human annotations
- Control-region false positive pruning (97.9% reduction)

### 2.4 Report Generation
- HTML (cyberpunk-styled dashboard, Gradio web UI)
- PDF (professional forensic audit format)
- DOCX (editable Word document)
- JSON (machine-readable for downstream integration)

### 2.5 Human-in-the-Loop
- Expert annotation interface for validating/suppressing findings
- Annotations feed back into control-region pruning
- Threshold tuning via LCM Sensitivity slider (0.5–0.9)

---

## 3. Non-Functional Requirements

### 3.1 Performance
- 85 pytest tests, ~7 seconds execution
- Docker health check: ~30 seconds container startup
- Progress tracking with ETA estimation for long-running analyses

### 3.2 Deployment
- Docker (recommended): multi-stage build, CPU-only, ~2GB image
- Local Python: pip install + manual PyTorch CPU wheel
- Non-root user execution in container (forensic user)
- Offline-ready: model weights pre-downloaded in builder stage

### 3.3 Security
- No API keys required (local model inference)
- No data leaves the machine
- Non-root container user
- Gradio analytics disabled

---

## 4. Technology Stack

### 4.1 Backend (Python 3.11+)
- **Framework**: Gradio (web UI) + FastAPI-style async pipeline
- **ML**: sentence-transformers (LaBSE / all-MiniLM-L6-v2), scikit-learn, numpy
- **PDF**: PyPDF2, pdfplumber
- **Reports**: reportlab, fpdf2
- **Testing**: pytest (85 tests)

### 4.2 Frontend (TypeScript/React via Vite)
- React + TypeScript
- Tailwind CSS
- Vite build system

### 4.3 Infrastructure
- Docker + docker-compose
- Multi-stage Dockerfile (builder → runtime)
- Netlify config (frontend hosting)

---

## 5. Model Dependencies

| Model | Purpose | Size |
|-------|---------|------|
| `sentence-transformers/all-MiniLM-L6-v2` | Sentence embeddings (default) | ~90MB |
| `sentence-transformers/LaBSE` | Alternative for multilingual/legal text | ~768-dim |
| `wtp-canine-medium` | Sentence splitting | — |
| `torch==2.10.0` (CPU) | Model inference backend | — |

**Note**: Torch is NOT in requirements.txt — installed separately in Dockerfile from PyTorch CPU wheel index to avoid ~3GB CUDA wheels.

---

## 6. Repository Structure (Key Paths)

```
hybrid_2026/
├── backend/                    # Python backend services
│   ├── app.py                  # Main Gradio entry / pipeline
│   ├── forensic_pipeline.py    # Multi-modal contradiction detection
│   └── modules/                 # Core logic modules
│       ├── document_processor.py
│       ├── lcm_engine.py
│       ├── entity_extractor.py
│       ├── number_extractor.py
│       ├── pdf_processor.py
│       └── report_generator.py
├── frontend/                   # React TypeScript UI
├── scripts/                    # Benchmarks + diagnostics
├── tests/                      # 85 pytest tests
├── data/                       # Ground truth + synthetic PDFs
├── outputs/                    # Generated reports (gitignored)
├── Dockerfile                  # Multi-stage container build
├── docker-compose.yml
├── requirements.txt            # Python dependencies
└── README.md                   # User-facing documentation
```

---

## 7. Known Issues / Technical Debt

1. **Push timeout**: `git push origin main` occasionally times out due to network or large file size limits (env_windows/, model_cache/ exceed 100MB GitHub limit).
2. **Windows line endings**: `.gitignore` handles LF→CRLF conversion warnings.
3. **Model cache**: `model_cache/` is gitignored; first run downloads ~90MB weights.
4. **Large binary exclusions**: `.pdf`, `.zip`, `env_windows/`, `model_cache/` excluded from git tracking.

---

## 8. Migration Checklist (Shipping to Another System)

### 8.1 Prerequisites
- [ ] Python 3.11+
- [ ] Git
- [ ] Docker (optional, recommended)
- [ ] 5GB free disk space

### 8.2 Clone
```bash
git clone https://github.com/orange-05/hybrid_2026.git
cd hybrid_2026
```

### 8.3 Option A: Docker (Recommended)
```bash
docker compose up -d
# Access: http://localhost:7860/
```

### 8.4 Option B: Local Python
```bash
pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python backend/app.py
```

### 8.5 Verification
```bash
python -m pytest tests/ -v  # 85 tests
```

### 8.6 First Use Workflow
1. Open `http://localhost:7860/`
2. Upload PDF (annual report / SEC filing / IPO prospectus)
3. Adjust LCM Sensitivity (default 0.70)
4. Click Analyze
5. Download reports (PDF / DOCX / HTML / JSON)

---

## 9. Configuration Reference

### 9.1 Environment Variables
| Variable | Default | Purpose |
|----------|---------|---------|
| `TRANSFORMERS_CACHE` | `/app/model_cache` | HF model cache |
| `HF_HOME` | `~/.cache/huggingface` | HuggingFace home |
| `GRADIO_ANALYTICS_ENABLED` | `False` | Disable telemetry |

### 9.2 LCM Sensitivity
- 0.50–0.60: High recall, more contradictions
- 0.70: Balanced (default)
- 0.80–0.90: High precision, fewer contradictions

---

## 10. Benchmark Reference

| Metric | Value |
|--------|-------|
| Detection Rate | 83.3% (5/6 planted) |
| Precision | ~85% (human-validated) |
| Recall | ~80% (human-validated) |
| F1 Score | ~83% |
| FP Reduction | 142 → 3 (97.9%) |
| Tests | 85 pytest |
| Max Document Tested | 422 pages |

---

## 11. Contradiction Types (11)

1. NUMERIC_FINANCIAL_MISMATCH
2. DEBT_POSITION_CONFLICT
3. INTENT_CONTRADICTION
4. NUMERIC_MISMATCH_LIABILITY
5. NUMERIC_MISMATCH_DEBT
6. NUMERIC_MISMATCH_TAX
7. NUMERIC_MISMATCH_PROFIT
8. NUMERIC_MISMATCH_INCOME
9. NUMERIC_MISMATCH_ASSET
10. NUMERIC_MISMATCH_PAYABLES
11. NUMERIC_MISMATCH_EQUITY

---

## 12. License & Contact

- **License**: MIT
- **Repo**: https://github.com/orange-05/hybrid_2026
- **Issues / Discussions**: GitHub Issues / Discussions

---

*This document is for personal reference when shipping or migrating the project. For user-facing docs, see README.md.*
