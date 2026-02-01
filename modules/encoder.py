import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer

class ConceptEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        # Force CPU to avoid VRAM overhead on your laptop
        self.device = "cpu"
        print(f"🔧 Initializing Speed Encoder (MiniLM) on {self.device.upper()}...")
        
        # Load the Speed Model
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=self.device)
        
        # The 1024-Dimension Projection Layer (Research Requirement)
        self.projection = nn.Linear(384, 1024).to(self.device)
        
        # Set entire module to evaluation mode (Safety Lock)
        self.eval()

    def encode(self, texts, batch_size=32):
        """
        Generates 1024-dimension vectors safely using No-Grad mode.
        """
        # CRITICAL FIX: torch.no_grad() prevents the "Backward" error
        # It tells PyTorch: "We are just looking, not learning."
        with torch.no_grad():
            # 1. Get Base Embeddings (Fast)
            embeddings_small = self.model.encode(
                texts, 
                batch_size=batch_size, 
                convert_to_tensor=True, 
                show_progress_bar=True,
                device=self.device
            )
            
            # 2. Project to Concept Space
            # This is where it crashed before. Now it is safe.
            embeddings_1024 = self.projection(embeddings_small)
            
        return embeddings_1024