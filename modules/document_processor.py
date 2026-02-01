import PyPDF2
import torch
import re
import time
import random
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

class DocumentProcessor:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)

    def process_document(self, pdf_path: str, max_sentences: int = 5000) -> Dict[str, Any]:
        sentences_raw = []
        with open(pdf_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    # Clean and segment
                    clean_text = re.sub(r'\s+', ' ', text).strip()
                    parts = re.split(r'[.!?]+\s+', clean_text)
                    for p in parts:
                        if len(p) > 35:
                            sentences_raw.append({
                                'text': p[:400], 
                                'page_num': i + 1, 
                                'section': f"Page_{i+1}"
                            })
                if i % 50 == 0: print(f"  ... Reading Page {i}")

        # Smart Sampling to maintain context
        if len(sentences_raw) > max_sentences:
            sentences_raw = random.sample(sentences_raw, max_sentences)
            sentences_raw.sort(key=lambda x: x['page_num'])

        # Vectorized Encoding
        texts = [s['text'] for s in sentences_raw]
        embeddings = self.model.encode(texts, batch_size=32, convert_to_numpy=True, normalize_embeddings=True)

        for idx, s in enumerate(sentences_raw):
            s['embedding'] = embeddings[idx]
            s['sentence_id'] = idx
            # Simplified Entity Extraction
            keywords = {'revenue', 'profit', 'debt', 'risk', 'asset'}
            s['entities'] = keywords.intersection(set(re.findall(r'\b\w+\b', s['text'].lower())))

        return {
            'sentences': sentences_raw, 
            'metadata': {'total_pages': len(pdf.pages), 'total_sentences': len(sentences_raw)}
        }