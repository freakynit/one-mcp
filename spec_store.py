from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from typing import List, Dict, Any
from pathlib import Path


class SpecStore:
    def __init__(self, storage_path: str = "spec_embeddings.json"):
        self.specs: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray = None
        self.storage_path = Path(storage_path)
        self.model_name = 'all-MiniLM-L6-v2'
        self.model = SentenceTransformer(self.model_name)
        self.load_from_disk()
    
    def add_specs(self, specs: List[Dict[str, Any]]):
        """Add specs and their embeddings to storage"""
        for spec in specs:
            # Serialize with name and description first
            serialized = self._serialize_spec(spec)
            embedding = self.model.encode(serialized)
            
            self.specs.append({
                "original": spec,
                "embedding": embedding.tolist()
            })
        
        # Update embeddings matrix
        self._update_embeddings_matrix()
        self.save_to_disk()
    
    def _serialize_spec(self, spec: Dict[str, Any]) -> str:
        """Serialize spec with name and description first"""
        parts = []
        
        # Prioritize name and description
        if "name" in spec:
            parts.append(f"Name: {spec['name']}")
        if "description" in spec:
            parts.append(f"Description: {spec['description']}")
        
        # Add remaining fields
        remaining = {k: v for k, v in spec.items() 
                    if k not in ["name", "description"]}
        if remaining:
            parts.append(json.dumps(remaining))
        
        return " | ".join(parts)
    
    def _update_embeddings_matrix(self):
        """Update the embeddings numpy array"""
        if self.specs:
            self.embeddings = np.array([s["embedding"] for s in self.specs])
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar specs using cosine similarity"""
        if not self.specs:
            return []
        
        # Create query embedding
        query_embedding = self.model.encode(query).reshape(1, -1)
        
        # Compute cosine similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top k indices
        actual_k = min(k, len(self.specs))
        top_k_indices = np.argsort(similarities)[::-1][:actual_k]
        
        # Return original specs with similarity scores
        results = []
        for idx in top_k_indices:
            results.append({
                "spec": self.specs[idx]["original"],
                "similarity_score": float(similarities[idx])
            })
        
        return results
    
    def save_to_disk(self):
        """Save specs and embeddings to disk"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.specs, f, indent=2)
    
    def load_from_disk(self):
        """Load specs and embeddings from disk"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    self.specs = json.load(f)
                self._update_embeddings_matrix()
                print(f"Loaded {len(self.specs)} specs from disk")
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error loading specs from disk: {e}")
                self.specs = []
