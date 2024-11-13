# src/embeddings.py
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingsHandler:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the embeddings model."""
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for a list of texts."""
        try:
            embeddings = self.model.encode(texts, show_progress_bar=True)
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return []

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        return self.model.get_sentence_embedding_dimension()