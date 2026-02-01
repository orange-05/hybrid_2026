"""
Report Generation Module
Generates professional forensic audit reports
"""

from typing import List, Dict
import logging
from datetime import datetime
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate professional audit reports from contradiction data"""
    
    def __init__(self):
        self.report_data = {}
        # Create outputs directory if it doesn't exist
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_executive_summary(self, contradictions: List, metadata: Dict) -> Dict:
        """Generate executive summary statistics"""
        
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        type_counts = {}
        
        for c in contradictions:
            # Safe severity extraction
            try:
                severity = c.get('severity', 'LOW') if isinstance(c, dict) else getattr(c, 'severity', 'LOW')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            except:
                severity_counts['LOW'] += 1
            
            # Safe type extraction
            try:
                ctype = c.get('contradiction_type', 'UNKNOWN') if isinstance(c, dict) else getattr(c, 'contradiction_type', 'UNKNOWN')
                type_counts[ctype] = type_counts.get(ctype, 0) + 1
            except:
                type_counts['UNKNOWN'] = type_counts.get('UNKNOWN', 0) + 1
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(contradictions)
        
        return {
            "total_contradictions": len(contradictions),
            "severity_breakdown": severity_counts,
            "type_breakdown": type_counts,
            "risk_score": risk_score,
            "document_pages": metadata.get('total_pages', 0),
            "sentences_analyzed": metadata.get('total_sentences', 0)
        }
    
    def _calculate_risk_score(self, contradictions: List) -> int:
        """Calculate risk score 0-100"""
        if not contradictions:
            return 0
        
        severity_weights = {
            "CRITICAL": 25,
            "HIGH": 15,
            "MEDIUM": 8,
            "LOW": 3
        }
        
        score = 0
        for c in contradictions:
            try:
                severity = c.get('severity', 'LOW') if isinstance(c, dict) else getattr(c, 'severity', 'LOW')
                score += severity_weights.get(severity, 0)
            except:
                score += 3  # Default LOW weight
        
        return min(100, score)
    
    def generate_detailed_findings(self, contradictions: List) -> List[Dict]:
        """Generate detailed findings for each contradiction"""
        
        findings = []
        
        for idx, c in enumerate(contradictions, 1):
            try:
                # Handle both dict and object types
                if isinstance(c, dict):
                    finding = {
                        "finding_id": idx,
                        "severity": c.get('severity', 'LOW'),
                        "type": c.get('contradiction_type', 'GENERAL_INCONSISTENCY'),
                        "score": round(c.get('similarity', 0), 3),
                        "page_1": c.get('page_a', '?'),
                        "page_2": c.get('page_b', '?'),
                        "statement_1": c.get('text_a', 'N/A'),
                        "statement_2": c.get('text_b', 'N/A'),
                        "entity_overlap": [],
                        "explanation": f"Logical inconsistency detected (Score: {c.get('similarity', 0):.3f})"
                    }
                else:
                    finding = {
                        "finding_id": idx,
                        "severity": getattr(c, 'severity', 'LOW'),
                        "type": getattr(c, 'contradiction_type', 'GENERAL_INCONSISTENCY'),
                        "score": round(getattr(c, 'score', 0), 3),
                        "page_1": getattr(getattr(c, 'sentence1', None), 'page_num', '?') if hasattr(c, 'sentence1') else '?',
                        "page_2": getattr(getattr(c, 'sentence2', None), 'page_num', '?') if hasattr(c, 'sentence2') else '?',
                        "statement_1": getattr(getattr(c, 'sentence1', None), 'text', 'N/A') if hasattr(c, 'sentence1') else 'N/A',
                        "statement_2": getattr(getattr(c, 'sentence2', None), 'text', 'N/A') if hasattr(c, 'sentence2') else 'N/A',
                        "entity_overlap": list(getattr(c, 'entity_overlap', [])),
                        "explanation": self._generate_explanation(c)
                    }
                
                findings.append(finding)
            except Exception as e:
                logger.error(f"Error processing contradiction {idx}: {e}")
                # Add a placeholder finding
                findings.append({
                    "finding_id": idx,
                    "severity": "LOW",
                    "type": "ERROR",
                    "score": 0,
                    "page_1": "?",
                    "page_2": "?",
                    "statement_1": "Error processing contradiction",
                    "statement_2": str(e),
                    "entity_overlap": [],
                    "explanation": f"Error processing this contradiction: {e}"
                })
        
        return findings
    
    def _generate_explanation(self, contradiction) -> str:
        """Generate human-readable explanation"""
        
        try:
            if isinstance(contradiction, dict):
                return f"Logical inconsistency detected with similarity score {contradiction.get('similarity', 0):.3f}"
            
            page1 = getattr(getattr(contradiction, 'sentence1', None), 'page_num', '?')
            page2 = getattr(getattr(contradiction, 'sentence2', None), 'page_num', '?')
            ctype = getattr(contradiction, 'contradiction_type', 'GENERAL_INCONSISTENCY')
            
            explanations = {
                "FINANCIAL_STATEMENT": f"Financial inconsistency between pages {page1} and {page2}.",
                "RISK_DISCLOSURE": f"Risk disclosure contradiction found between pages {page1} and {page2}.",
                "PERFORMANCE_METRIC": f"Contradictory performance metrics on pages {page1} and {page2}.",
                "OPERATIONAL_STATUS": f"Operational status inconsistency between pages {page1} and {page2}.",
                "GENERAL_INCONSISTENCY": f"Logical inconsistency detected between pages {page1} and {page2}."
            }
            
            base_explanation = explanations.get(ctype, "Logical inconsistency detected.")
            
            entity_overlap = getattr(contradiction, 'entity_overlap', set())
            if entity_overlap:
                entities_str = ", ".join(list(entity_overlap)[:3])
                base_explanation += f" Related entities: {entities_str}."
            
            severity = getattr(contradiction, 'severity', 'LOW')
            if severity == "CRITICAL":
                base_explanation += " This is a critical issue requiring immediate attention."
            
            return base_explanation
        
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Error generating explanation for this contradiction."
    
    def generate_html_report(self, contradictions: List, metadata: Dict, filename: str = None):
        """
        Generate HTML report
        
        Args:
            contradictions: List of contradiction objects
            metadata: Document metadata
            filename: Output filename (auto-generated if None)
        """
        
        try:
            executive_summary = self.generate_executive_summary(contradictions, metadata)
            detailed_findings = self.generate_detailed_findings(contradictions)
            
            # Auto-generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(self.output_dir, f"forensic_report_{timestamp}.html")
            else:
                # Ensure filename is in outputs directory
                if not os.path.dirname(filename):
                    filename = os.path.join(self.output_dir, filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else self.output_dir, exist_ok=True)
            
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Forensic Audit Report</title>
    <style>
        body {{ 
            font-family: 'Arial', 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%); 
            color: #e0e0e0; 
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{ 
            color: #00ffff; 
            text-align: center; 
            font-size: 36px;
            text-shadow: 0 0 20px rgba(0,255,255,0.5);
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #8b9dc3;
            font-size: 14px;
            letter-spacing: 2px;
            margin-bottom: 30px;
        }}
        .summary {{ 
            background: rgba(26, 26, 26, 0.95); 
            padding: 25px; 
            border-radius: 12px; 
            margin: 20px 0;
            border: 1px solid rgba(0,255,255,0.3);
            box-shadow: 0 0 20px rgba(0,255,255,0.1);
        }}
        .summary h2 {{
            color: #00ffff;
            margin-top: 0;
            font-size: 24px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .stat-box {{
            background: rgba(0,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #00ffff;
        }}
        .stat-label {{
            color: #8b9dc3;
            font-size: 12px;
            text-transform: uppercase;
        }}
        .stat-value {{
            color: #00ffff;
            font-size: 24px;
            font-weight: bold;
            margin-top: 5px;
        }}
        .finding {{ 
            background: rgba(26, 26, 26, 0.95); 
            padding: 20px; 
            margin: 15px 0; 
            border-left: 4px solid #00ffff;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        .finding:hover {{
            box-shadow: 0 0 20px rgba(0,255,255,0.2);
            transform: translateX(5px);
        }}
        .finding.CRITICAL {{ border-left-color: #ff0040; }}
        .finding.HIGH {{ border-left-color: #ff6b00; }}
        .finding.MEDIUM {{ border-left-color: #ffaa00; }}
        .finding.LOW {{ border-left-color: #00ff00; }}
        .finding h3 {{
            color: #00ffff;
            margin-top: 0;
            font-size: 18px;
        }}
        .finding-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin: 15px 0;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 5px;
        }}
        .finding-meta-item {{
            font-size: 13px;
        }}
        .finding-meta-label {{
            color: #8b9dc3;
            font-size: 11px;
            text-transform: uppercase;
        }}
        .finding-meta-value {{
            color: #00ffff;
            font-weight: bold;
        }}
        .statement-box {{
            background: rgba(0,0,0,0.5);
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 2px solid rgba(0,255,255,0.5);
        }}
        .statement-label {{
            color: #00ffff;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .statement-text {{
            color: #e0e0e0;
            line-height: 1.6;
        }}
        .severity-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .severity-CRITICAL {{ background: #ff0040; color: white; }}
        .severity-HIGH {{ background: #ff6b00; color: white; }}
        .severity-MEDIUM {{ background: #ffaa00; color: black; }}
        .severity-LOW {{ background: #00ff00; color: black; }}
        .explanation {{
            margin-top: 15px;
            padding: 12px;
            background: rgba(0,255,255,0.05);
            border-radius: 5px;
            font-style: italic;
            color: #b0d4e0;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(0,255,255,0.3);
            color: #8b9dc3;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 FORENSIC AUDIT REPORT</h1>
        <div class="subtitle">HYBRID LCM-LLM ARCHITECTURE</div>
        
        <div class="summary">
            <h2>📊 Executive Summary</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-label">Total Contradictions</div>
                    <div class="stat-value">{executive_summary['total_contradictions']}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Risk Score</div>
                    <div class="stat-value">{executive_summary['risk_score']}/100</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Document Pages</div>
                    <div class="stat-value">{executive_summary['document_pages']}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Sentences Analyzed</div>
                    <div class="stat-value">{executive_summary['sentences_analyzed']}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Critical Issues</div>
                    <div class="stat-value">{executive_summary['severity_breakdown']['CRITICAL']}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">High Priority</div>
                    <div class="stat-value">{executive_summary['severity_breakdown']['HIGH']}</div>
                </div>
            </div>
        </div>
        
        <h2 style="color: #00ffff; margin-top: 40px;">🔍 Detailed Findings</h2>
"""
            
            if detailed_findings:
                for finding in detailed_findings:
                    severity = finding.get('severity', 'LOW')
                    html_content += f"""
        <div class="finding {severity}">
            <h3>
                Finding #{finding['finding_id']} 
                <span class="severity-badge severity-{severity}">{severity}</span>
            </h3>
            
            <div class="finding-meta">
                <div class="finding-meta-item">
                    <div class="finding-meta-label">Pages</div>
                    <div class="finding-meta-value">{finding['page_1']} ↔ {finding['page_2']}</div>
                </div>
                <div class="finding-meta-item">
                    <div class="finding-meta-label">Contradiction Score</div>
                    <div class="finding-meta-value">{finding['score']}</div>
                </div>
                <div class="finding-meta-item">
                    <div class="finding-meta-label">Type</div>
                    <div class="finding-meta-value">{finding['type']}</div>
                </div>
            </div>
            
            <div class="statement-box">
                <div class="statement-label">📄 Statement from Page {finding['page_1']}:</div>
                <div class="statement-text">"{finding['statement_1']}"</div>
            </div>
            
            <div class="statement-box">
                <div class="statement-label">📄 Statement from Page {finding['page_2']}:</div>
                <div class="statement-text">"{finding['statement_2']}"</div>
            </div>
            
            <div class="explanation">
                <strong>Analysis:</strong> {finding['explanation']}
            </div>
        </div>
"""
            else:
                html_content += """
        <div class="summary">
            <p style="text-align: center; color: #00ff00; font-size: 18px;">
                ✅ No contradictions detected. Document appears logically coherent.
            </p>
        </div>
"""
            
            html_content += f"""
        <div class="footer">
            <p>Report generated by Agentic Financial Forensics v2.1</p>
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Write file with proper error handling
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ HTML report saved: {filename}")
            return filename
        
        except Exception as e:
            logger.error(f"❌ Error generating HTML report: {e}")
            raise
    
    def export_to_json(self, contradictions: List, metadata: Dict, filename: str = None):
        """
        Export report to JSON format
        
        Args:
            contradictions: List of contradiction objects
            metadata: Document metadata
            filename: Output filename (auto-generated if None)
        """
        
        try:
            executive_summary = self.generate_executive_summary(contradictions, metadata)
            detailed_findings = self.generate_detailed_findings(contradictions)
            
            # Auto-generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(self.output_dir, f"forensic_report_{timestamp}.json")
            else:
                # Ensure filename is in outputs directory
                if not os.path.dirname(filename):
                    filename = os.path.join(self.output_dir, filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else self.output_dir, exist_ok=True)
            
            report = {
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "engine": "Hybrid LCM-LLM Architecture",
                    "version": "2.1"
                },
                "executive_summary": executive_summary,
                "detailed_findings": detailed_findings,
                "document_metadata": metadata
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ JSON report saved: {filename}")
            return filename
        
        except Exception as e:
            logger.error(f"❌ Error exporting to JSON: {e}")
            raise


# Alias for backward compatibility
ForensicReportGenerator = ReportGenerator