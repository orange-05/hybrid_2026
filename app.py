"""
Agentic Financial Forensics - CLEAN MASTER BUILD
Memory-Optimized for 422-Page Forensic Audits
"""
import gradio as gr
import os
import sys
import logging
from datetime import datetime

# CRITICAL: Ensures modules in the subfolder are found
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.document_processor import DocumentProcessor
from modules.lcm_engine import HierarchicalLCM
from modules.report_generator import ForensicReportGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state to prevent re-loading the 90MB model
processor_instance = None

def run_forensic_scan(file, threshold, progress=gr.Progress()):
    global processor_instance
    if file is None: return "⚠️ Please upload a PDF.", None, None, None
    
    try:
        # Step 1: Initialize
        if processor_instance is None:
            progress(0, desc="🚀 Initializing 90MB MiniLM Model...")
            processor_instance = DocumentProcessor()
        
        # Step 2: Extract and Encode
        progress(0.2, desc="📂 Processing 422-Page Structure...")
        result = processor_instance.process_document(file.name)
        
        # Step 3: Hierarchical Detection
        progress(0.6, desc="🔍 Running Hierarchical LCM Analysis...")
        lcm = HierarchicalLCM(threshold=threshold)
        
        for s in result['sentences']:
            lcm.add_sentence(
                text=s['text'], 
                page_num=s['page_num'], 
                section=s['section'],
                embedding=s['embedding'], 
                entities=s['entities'], 
                sentence_id=s['sentence_id']
            )
            
        contradictions = lcm.detect_contradictions()
        
        # Step 4: Report Generation
        progress(0.9, desc="📊 Compiling Forensic Audit...")
        report_gen = ForensicReportGenerator()
        summary_data = report_gen.generate_executive_summary(contradictions, result['metadata'])
        
        # Format Table for Gradio
        table = [
            ["Pages Detected", f"{summary_data['document_pages']}"],
            ["Logical Drifts", f"{summary_data['total_contradictions']}"],
            ["Risk Score", f"{summary_data['risk_score']}/100"]
        ]
        
        # Generate HTML
        os.makedirs("outputs", exist_ok=True)
        report_path = f"outputs/audit_{int(datetime.now().timestamp())}.html"
        report_gen.generate_html_report(contradictions, result['metadata'], report_path)
        
        return "✅ Forensic Audit Complete", table, report_path, report_path

    except Exception as e:
        logger.error(f"System Crash: {e}")
        return f"❌ CRITICAL ERROR: {str(e)}", None, None, None

# --- UI DESIGN ---
with gr.Blocks(theme=gr.themes.Base(primary_hue="cyan"), css="body {background: #050505;}") as demo:
    gr.HTML("<h1 style='text-align:center; color:#00ffff;'>AGENTIC FINANCIAL FORENSICS</h1>")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_in = gr.File(label="Evidence Ingestion (PDF)", file_types=[".pdf"])
            sens = gr.Slider(0.5, 0.9, value=0.70, label="Contradiction Sensitivity")
            btn = gr.Button("🔍 INITIATE SYSTEM SCAN", variant="primary")
        
        with gr.Column(scale=2):
            status = gr.Markdown("**System Status:** Ready")
            summary_table = gr.Dataframe(headers=["Metric", "Value"], row_count=3)
            report_view = gr.File(label="📥 Download Forensic Audit")

    btn.click(run_forensic_scan, [file_in, sens], [status, summary_table, report_view, report_view])

if __name__ == "__main__":
    demo.launch(server_port=7860)