import torch
from sentence_transformers import SentenceTransformer
from wtpsplit import WtPSplitter
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class AgenticForensicsEngine:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Initializing Forensic Model on {self.device}...")
        
        # Using LaBSE as seen in your logs (It's robust for legal text)
        self.model = SentenceTransformer('sentence-transformers/LaBSE', device=self.device)
        
        # Initialize Splitter
        self.splitter = WtPSplitter(model_name="wtp-canine-medium")
        print("✅ Engine Online & Ready.")

    def ingest_document(self, text):
        # Split text into sentences
        return self.splitter.split(text[:100000], lang_code="en")

    def compute_concept_vectors(self, sents):
        # CRITICAL FIX: We force 'convert_to_tensor=True' to prevent the crash
        embeddings = self.model.encode(sents, convert_to_tensor=True, show_progress_bar=True)
        return embeddings

    def detect_logical_drift(self, sents, embeddings):
        # Convert Tensor to Numpy for similarity calculation (Safe transition)
        vecs = embeddings.cpu().detach().numpy()
        sim_matrix = cosine_similarity(vecs)
        
        alerts = []
        for i in range(len(sents)):
            for j in range(i + 1, len(sents)):
                score = sim_matrix[i][j]
                # Drift Logic: Context matches (0.65+) but not identical (<0.85)
                if 0.65 < score < 0.85: 
                    alerts.append({
                        "text_a": sents[i], 
                        "text_b": sents[j], 
                        "similarity": float(score)
                    })
                if len(alerts) > 5: break
            if len(alerts) > 5: break
        return alerts

    def simulate_world_event(self, base, impact):
        return base * (1 + impact + np.random.normal(0, 0.05))
