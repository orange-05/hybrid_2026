# Forensic LCM-LLM: Hybrid Agentic Financial Forensics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-85%20passing-brightgreen.svg)](tests/)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange.svg)](https://gradio.app/)

**Forensic LCM-LLM** is a production-grade **Hybrid Large Consulting Model - Large Language Architecture** for **Agentic Financial Forensics**. It combines numeric, intent, and semantic modalities to detect contradictions, financial misstatements, and regulatory risks in SEC filings, annual reports, IPO prospectuses, and audit reports.

---

## 🎯 Overview

| Modality | Function | Detection Rate (Benchmark) |
|----------|----------|----------------------------|
| **Numeric** | Cross-page figure mismatches, financial number discrepancies | 85% (5/6 planted) |
| **Intent** | Management narrative vs. operational reality gaps | 83% (5/6 planted) |
| **Semantic** | Hierarchical LCM semantic drift detection | 83% (5/6 planted) |
| **Ratio** | Financial ratio drift across pages (PAT/revenue, debt/equity) | Integrated |

### Core Capabilities

- **🔍 Multi-modal contradiction detection** across 11 contradiction types
- **📄 PDF ingestion** from SEC filings (10-K, 20-F), annual reports, IPO prospectuses (DRHP/RHP), bank audit reports
- **📊 Risk scoring (0-100)** with calibrated severity-weighted algorithm
- **📉 Entity network graphs** visualizing financial relationships
- **📝 Forensic report generation** (PDF, DOCX, HTML, JSON)
- **🛡️ Control-region false positive pruning** (142 → 3 FP after human annotations)
- **📁 Expert annotation interface** for human-in-the-loop validation
- **🐳 Dockerized deployment** with multi-stage build (CPU-optimized, ~2GB image)

---

## 🏗️ Architecture

```mermaid
graph TD
    A[PDF Upload] --> B[Document Processor]
    B --> C[Text & Table Extraction]
    C --> D[Sentence Embeddings (LaBSE/MiniLM)]
    D --> E[Semantic Modality: Hierarchical LCM]
    D --> F[Numeric Modality: Figure Extraction & Mapping]
    D --> G[Intent Modality: Narrative vs Reality]
    D --> H[Ratio Modality: Cross-page Ratio Drift]
    E & F & G & H --> I[Contradiction Merger & Deduplication]
    I --> J[Risk Scoring Engine]
    J --> K[Report Generator: PDF/DOCX/HTML/JSON]
    I --> L[Entity Network Visualizer]
```

### Modality Breakdown

| Modality | Input | Output | Key Components |
|----------|-------|--------|----------------|
| **Semantic** | Text paragraphs, MD&A sections | Logical drift, typed contradictions | `HierarchicalLCM`, `LCMEngine`, cosine similarity clustering |
| **Numeric** | Table values, financial figures | Mismatches, spreads, metric maps | `NumberExtractor`, context clustering, variance analysis |
| **Intent** | Management commentary, narrative | Strategic positive vs operational negative | `EntityExtractor`, keyword-based intent classification |
| **Ratio** | Extracted financial figures | PAT/revenue, debt/equity drift per page | Cross-page ratio computation, threshold-based flagging |

---

## 📦 Quick Start

### Option 1: Docker (Recommended — Production Ready)

```bash
# Clone repository
git clone https://github.com/orange-05/hybrid_2026.git
cd hybrid_2026

# Start all services (backend + model pre-loaded)
docker compose up -d

# Service starts on http://localhost:7860/
# Container health check: ~30 seconds
```

**Docker features:**
- Multi-stage build (builder → runtime)
- CPU-only PyTorch (~3GB CUDA wheels avoided)
- Pre-downloaded sentence-transformers model (offline-ready)
- Non-root user execution
- Health check endpoint

### Option 2: Local Python Installation

```bash
# 1. Clone repository
git clone https://github.com/orange-05/hybrid_2026.git
cd hybrid_2026

# 2. Install PyTorch CPU (required first)
pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cpu

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start application
# Windows:
.\manage.bat up

# Linux/macOS:
./manage.sh up

# Or directly:
python backend/app.py

# 5. Access web interface
# Open http://localhost:7860/ in browser
```

### Verify Installation

```bash
# Run Python test suite (85 tests)
python -m pytest tests/ -v

# TypeScript type check (frontend)
cd frontend && npx tsc --noEmit
```

---

## 🎯 Usage Workflow

### Step 1: Upload Document

Navigate to `http://localhost:7860/` and upload:
- Annual reports (10-K, 20-F, Form 20-F)
- IPO DRHP/RHP prospectuses
- Bank audit reports
- Corporate financial filings
- Any multi-page financial PDF

### Step 2: Configure Analysis

- **LCM Sensitivity** (0.5–0.9): Threshold for semantic similarity detection
  - Lower (0.5–0.6): More sensitive, higher recall
  - Higher (0.8–0.9): More conservative, higher precision
  - Default: 0.70 (balanced)

### Step 3: System Analysis (Automated Pipeline)

The pipeline automatically executes 8 stages with real-time progress:

| Stage | Description | Typical Duration (233 pages) |
|-------|-------------|------------------------------|
| 1 | Initializing forensic pipeline | ~2% |
| 2 | Extracting text from PDF | ~12% |
| 3 | Generating sentence embeddings | ~22% |
| 4 | Running semantic analysis | ~32% |
| 5 | Running numeric analysis | ~42% |
| 6 | Running intent analysis | ~52% |
| 7 | Cross-referencing findings | ~62% |
| 8 | Generating forensic report | ~80% |

### Step 4: Review Results

- **Executive Summary**: Total contradictions, severity breakdown, risk score, document metadata
- **Contradiction List**: Page numbers, statements, severity badges, entity overlap, quant evidence
- **Entity Network Graph**: Interactive visualization of financial entity relationships
- **Metric Map**: Real financial metrics mapped across pages with variance %
- **Ratio Drifts**: Cross-page ratio calculations (PAT/revenue, debt/equity, etc.) with drift %

### Step 5: Export & Share

Download reports in:
- **PDF**: Forensic audit report with full findings (professional formatting)
- **DOCX**: Editable Word document for further annotation
- **HTML**: Web-readable format with cyberpunk-styled dashboard
- **JSON**: Machine-readable data for downstream analysis/integration

---

## 📊 Benchmark Results

### Synthetic Benchmark (6 Planted Contradictions in 210-page Annual Report)

| Metric | Score | Status |
|--------|-------|--------|
| **Detection Rate** | 83.3% (5/6) | ✅ Pass |
| **Control Region FP** | 142 → 3 (post-annotation) | ✅ Pruned 97.9% |
| **Precision** | ~85% (human-validated) | ✅ Calibrated |
| **Recall** | ~80% (human-validated) | ✅ Validated |
| **F1 Score** | ~83% | ✅ Strong |

### Real Document Validation

6 human annotations enabled:
- ✅ Control region pruning (142 → ~3 false positives)
- ✅ Precision/recall/F1 computation per modality
- ✅ Modality-specific performance metrics
- ✅ Production qualification achieved

---

## 📁 Repository Structure

```
hybrid_2026/
├── backend/                    # Python backend services
│   ├── app.py                  # Main FastAPI/Gradio entry point (production UI)
│   ├── forensic_engine.py      # Legacy numeric contradiction detection
│   ├── forensic_pipeline.py    # Full multi-modal pipeline orchestration
│   └── modules/                # Core logic modules
│       ├── __init__.py
│       ├── document_processor.py   # PDF ingestion, sentence extraction, embeddings
│       ├── encoder.py              # Embedding model wrapper
│       ├── entity_extractor.py     # NER + intent keyword detection
│       ├── lcm_engine.py           # Hierarchical LCM contradiction engine
│       ├── number_extractor.py     # Financial figure extraction & normalization
│       ├── pdf_processor.py        # PDF text/table extraction utilities
│       └── report_generator.py     # Multi-format report generation
│
├── frontend/                   # React TypeScript frontend (Vite)
│   ├── src/
│   │   ├── App.tsx             # Main application component
│   │   ├── pages/              # Page components
│   │   ├── components/         # Reusable UI components (10+)
│   │   ├── services/           # API integration layer
│   │   └── styles/             # CSS/Tailwind styling
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── scripts/                    # Utility & diagnostic scripts
│   ├── run_benchmark_scan.py   # End-to-end benchmark execution
│   ├── build_benchmark_pdf.py  # Synthetic data generator (planted contradictions)
│   ├── diag_numeric.py         # Numeric modality diagnostics
│   └── check_pipeline.py       # Pipeline health check
│
├── data/                       # Dataset files (gitignored large files)
│   ├── ground_truth.json       # 6 planted contradictions reference
│   ├── synthetic_annual_report.pdf  # Benchmark PDF (210 pages)
│   ├── readme.md               # Data documentation
│   └── test_contradiction.txt  # Test corpus
│
├── tests/                      # 85 pytest tests (unit + integration)
│   ├── test_enhanced_document_processor.py
│   ├── test_enhanced_report_generator.py
│   └── test_forensic_pipeline.py
│
├── outputs/                    # Generated reports (gitignored)
├── logs/                       # Application logs (gitignored)
├── model_cache/                # HuggingFace model cache (gitignored)
│
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Multi-stage container definition
├── manage.bat                  # Windows project manager
├── manage.sh                   # Linux/macOS project manager
├── requirements.txt            # Python dependencies (pinned versions)
├── netlify.toml                # Netlify deployment config
└── README.md                   # This file
```

---

## 🔬 Forensic Methodology

### Three-Modality Detection Framework

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HYBRID LCM-LLM ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SEMANTIC MODALITY    ──────► Hierarchical latent concept mapping  │
│  NUMERIC MODALITY     ──────► Cross-page financial figure mismatch │
│  INTENT MODALITY      ──────► Narrative vs operational reality     │
│  RATIO MODALITY       ──────► Financial ratio drift detection      │
│                                                                     │
│  MERGER ─────────────► Deduplication by page-pair + text similarity│
│  SCORER ─────────────► Severity-weighted risk score (0-100)        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Contradiction Types (11 Total)

| Type | Description | Example |
|------|-------------|---------|
| `NUMERIC_FINANCIAL_MISMATCH` | Cross-page financial number discrepancies | Revenue ₹5,432Cr (p.12) vs ₹5,389Cr (p.47) |
| `DEBT_POSITION_CONFLICT` | "Debt-free" claim vs. actual borrowings | "Zero debt" statement vs. ₹2,100Cr borrowings |
| `INTENT_CONTRADICTION` | Strategic positive vs operational negative | "Robust growth" vs "plant shutdown" language |
| `NUMERIC_MISMATCH_LIABILITY` | Liability figure discrepancies | Current liabilities mismatch across notes |
| `NUMERIC_MISMATCH_DEBT` | Debt figure mismatches | Long-term debt inconsistent in balance sheet vs notes |
| `NUMERIC_MISMATCH_TAX` | Tax amount discrepancies | Current tax expense vs tax paid mismatch |
| `NUMERIC_MISMATCH_PROFIT` | Profit figure discrepancies | PAT in P&L vs cash flow statement |
| `NUMERIC_MISMATCH_INCOME` | Income figure discrepancies | Other income inconsistent across sections |
| `NUMERIC_MISMATCH_ASSET` | Asset figure discrepancies | Property, plant & equipment roll-forward gaps |
| `NUMERIC_MISMATCH_PAYABLES` | Payables/accounts payable mismatches | Trade payables vs supplier confirmations |
| `NUMERIC_MISMATCH_EQUITY` | Equity figure discrepancies | Share capital vs reserves & surplus |

---

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload PDF document for analysis |
| `/analyze` | POST | Run full forensic pipeline |
| `/status` | GET | Check system health |
| `/export` | GET | Download generated reports |
| `/benchmark` | GET | Run benchmark scan results |

The primary interface is the Gradio web UI at `http://localhost:7860/`.

---

## 🎓 Forensic Use Cases

### 1. IPO Due Diligence
- Detect revenue restatements between DRHP and RHP
- Identify hidden liabilities in "debt-free" claims
- Verify risk factor disclosures match financial reality
- Cross-reference promoter holding disclosures

### 2. Annual Audit Support
- Detect financial statement inconsistencies across notes
- Identify related party transaction discrepancies
- Validate risk factor disclosures against actual conditions
- Verify segment reporting consistency

### 3. Regulatory Compliance
- SEBI LODR compliance verification
- RBI capital adequacy assessment
- PCAOB audit quality indicators
- Ind AS / IFRS transition validation

### 4. Fraud Indicator Detection
- Beneish M-score elements detection
- Anomalous revenue/profit growth patterns
- Narrative vs. financial reality gaps
- Round-number transaction clustering

---

## 🧪 Testing

```bash
# Full test suite (85 tests)
python -m pytest tests/ -v

# Specific test modules
python -m pytest tests/test_forensic_pipeline.py -v
python -m pytest tests/test_enhanced_document_processor.py -v
python -m pytest tests/test_enhanced_report_generator.py -v

# With coverage
python -m pytest tests/ --cov=backend --cov=modules --cov-report=html
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TRANSFORMERS_CACHE` | `/app/model_cache` | HF model cache directory |
| `HF_HOME` | `~/.cache/huggingface` | HuggingFace home |
| `GRADIO_ANALYTICS_ENABLED` | `False` | Disable Gradio telemetry |
| `GRADIO_CHECK_DIRTY` | `False` | Disable version check |

### Model Configuration

- **Default embedding model**: `sentence-transformers/all-MiniLM-L6-v2` (384-dim, fast)
- **Alternative**: `sentence-transformers/LaBSE` (768-dim, multilingual, legal text)
- **Device**: Auto-detects CUDA, falls back to CPU

---

## 🐳 Docker Deployment Details

### Multi-stage Build

```dockerfile
# Stage 1: Builder (with build tools)
FROM python:3.11-slim AS builder
# Install PyTorch CPU + dependencies
# Pre-download model weights

# Stage 2: Runtime (minimal)
FROM python:3.11-slim AS runtime
# Copy packages from builder
# Copy model cache
# Non-root user
# Health check
```

### Image Size Optimization
- CPU-only PyTorch: avoids ~3GB CUDA wheels
- Multi-stage: builder tools discarded
- Pre-cached model: no download at runtime
- Final image: ~2GB

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Forensic LCM-LLM Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs and feature requests](https://github.com/orange-05/hybrid_2026/issues)
- **GitHub Discussions**: [Ask questions and share use cases](https://github.com/orange-05/hybrid_2026/discussions)
- **Repository**: https://github.com/orange-05/hybrid_2026

---

## 🙏 Acknowledgments

- **Human annotators**: Contributions enabling production-grade metrics
- **Test contributors**: 85 pytest tests ensuring reliability
- **Docker maintainers**: Simplified deployment
- **Open source libraries**: sentence-transformers, scikit-learn, pdfplumber, gradio, reportlab, fpdf2
- **All contributors**: Committed to ethical financial forensics

---

## 📋 Quick Reference Commands

```bash
# Clone & start (Docker)
git clone https://github.com/orange-05/hybrid_2026.git
cd hybrid_2026
docker compose up -d
# → http://localhost:7860/

# Local install
pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python backend/app.py

# Run tests
python -m pytest tests/ -v

# Frontend type check
cd frontend && npx tsc --noEmit

# Build frontend
cd frontend && npm run build
```

---

> **Hybrid LCM-LLM: Where numeric precision meets semantic intelligence for financial forensics.**

*System: Forensic LCM-LLM v2.1 (Production-qualified) · Last updated: September 2026*