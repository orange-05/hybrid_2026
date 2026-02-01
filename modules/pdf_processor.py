"""PDF Processing Module"""
import pdfplumber
import re
from typing import List, Dict
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Sentence:
    text: str
    page_num: int
    position: int
    section: str = "Unknown"

class PDFProcessor:
    def __init__(self):
        self.sentences: List[Sentence] = []
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Sentence]:
        logger.info(f"📄 Processing: {pdf_path}")
        all_sentences = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if not text:
                    continue
                
                sentences = self._segment_sentences(text)
                for pos, sent in enumerate(sentences):
                    if len(sent.strip()) > 10:
                        all_sentences.append(Sentence(sent.strip(), page_num, pos))
                
                if page_num % 50 == 0:
                    logger.info(f"✅ Processed {page_num} pages")
        
        self.sentences = all_sentences
        logger.info(f"📊 Total sentences: {len(all_sentences)}")
        return all_sentences
    
    def _segment_sentences(self, text: str) -> List[str]:
        text = text.replace('\n', ' ')
        return re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    def get_statistics(self) -> Dict:
        pages = set(s.page_num for s in self.sentences)
        return {
            "total_sentences": len(self.sentences),
            "total_pages": len(pages),
            "avg_per_page": round(len(self.sentences) / len(pages), 2) if pages else 0
        }

if __name__ == "__main__":
    print("✅ PDF Processor ready!")
