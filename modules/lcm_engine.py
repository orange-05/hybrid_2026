import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dataclasses import dataclass
from typing import List, Set

@dataclass
class Sentence:
    text: str
    page_num: int
    section: str
    embedding: np.ndarray
    entities: Set[str]
    sentence_id: int

@dataclass
class Contradiction:
    sentence1: Sentence
    sentence2: Sentence
    score: float
    severity: str
    contradiction_type: str
    entity_overlap: Set[str]

class LCMEngine:
    def __init__(self, threshold=0.70):
        self.threshold = threshold

    def detect_contradictions(self, sentences: List[Sentence], embeddings: np.ndarray) -> List[Contradiction]:
        sim_matrix = cosine_similarity(embeddings)
        mask = (sim_matrix > self.threshold) & (sim_matrix < 0.98)
        rows, cols = np.where(np.triu(mask, k=1))
        
        contradictions = []
        for r, c in zip(rows[:40], cols[:40]):
            s1, s2 = sentences[r], sentences[c]
            if abs(s1.page_num - s2.page_num) < 2: continue
            
            overlap = s1.entities & s2.entities
            sim_val = float(sim_matrix[r, c])
            
            # Severity Logic
            severity = "CRITICAL" if sim_val > 0.88 else "HIGH" if sim_val > 0.82 else "MEDIUM"
            
            contradictions.append(Contradiction(
                sentence1=s1, sentence2=s2, score=sim_val,
                severity=severity, contradiction_type="GENERAL_INCONSISTENCY",
                entity_overlap=overlap
            ))
        return contradictions

class HierarchicalLCM(LCMEngine):
    def __init__(self, threshold=0.65):
        super().__init__(threshold)
        self.sentences = []

    def add_sentence(self, text, page_num, section, embedding, entities, sentence_id):
        self.sentences.append(Sentence(text, page_num, section, embedding, entities, sentence_id))

    def detect_contradictions(self) -> List[Contradiction]:
        if not self.sentences: return []
        embs = np.vstack([s.embedding for s in self.sentences])
        return super().detect_contradictions(self.sentences, embs)