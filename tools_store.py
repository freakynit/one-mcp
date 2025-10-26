from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from typing import List, Dict, Any
from pathlib import Path
from logging_setup import get_logger

logger = get_logger(__name__)
tools_stores = {}

class ToolsStore:
    def __init__(self, storage_path: str = "tool_embeddings.json"):
        self.tools: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray = None
        self.storage_path = Path(storage_path)
        self.model_name = 'all-MiniLM-L6-v2'
        self.model = SentenceTransformer(self.model_name)
        self.load_from_disk()
    
    def add_tools(self, tools: List[Dict[str, Any]]):
        """Add tools and their embeddings to storage"""
        for tool in tools:
            # Serialize with name and description first
            serialized = self._serialize_tool(tool)
            embedding = self.model.encode(serialized)
            
            self.tools.append({
                "original": tool,
                "embedding": embedding.tolist()
            })
        
        # Update embeddings matrix
        self._update_embeddings_matrix()
        self.save_to_disk()
    
    def _serialize_tool(self, tool: Dict[str, Any]) -> str:
        """Serialize tool with name and description first"""
        parts = []
        
        # Prioritize name and description
        if "name" in tool:
            parts.append(f"Name: {tool['name']}")
        if "description" in tool:
            parts.append(f"Description: {tool['description']}")
        
        # Add remaining fields
        remaining = {k: v for k, v in tool.items() 
                    if k not in ["name", "description"]}
        if remaining:
            parts.append(json.dumps(remaining))
        
        return " | ".join(parts)
    
    def _update_embeddings_matrix(self):
        """Update the embeddings numpy array"""
        if self.tools:
            self.embeddings = np.array([s["embedding"] for s in self.tools])
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar tools using cosine similarity"""
        if not self.tools:
            return []
        
        # Create query embedding
        query_embedding = self.model.encode(query).reshape(1, -1)
        
        # Compute cosine similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top k indices
        actual_k = min(k, len(self.tools))
        top_k_indices = np.argsort(similarities)[::-1][:actual_k]
        
        # Return original tools with similarity scores
        results = []
        for idx in top_k_indices:
            results.append({
                "tool": self.tools[idx]["original"],
                "similarity_score": float(similarities[idx])
            })
        
        return results
    
    def delete_tools(self, tool_names: List[str]) -> Dict[str, Any]:
        """Delete tools by their names"""
        if not self.tools:
            return {"deleted_count": 0, "not_found": tool_names, "message": "No tools available to delete"}
        
        deleted_count = 0
        not_found = []
        initial_count = len(self.tools)
        
        # Create a new list without the tools to be deleted
        remaining_tools = []
        for tool_data in self.tools:
            tool_name = tool_data["original"].get("name", "")
            if tool_name in tool_names:
                deleted_count += 1
            else:
                remaining_tools.append(tool_data)
        
        # Check which tool names were not found
        found_names = set()
        for tool_data in self.tools:
            tool_name = tool_data["original"].get("name", "")
            if tool_name in tool_names:
                found_names.add(tool_name)
        
        not_found = [name for name in tool_names if name not in found_names]
        
        # Update the tools list
        self.tools = remaining_tools
        
        # Update embeddings matrix
        self._update_embeddings_matrix()
        
        # Save to disk
        self.save_to_disk()
        
        return {
            "deleted_count": deleted_count,
            "not_found": not_found,
            "total_tools_remaining": len(self.tools),
            "message": f"Successfully deleted {deleted_count} tools. {len(not_found)} tools not found."
        }
    
    def save_to_disk(self):
        """Save tools and embeddings to disk"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.tools, f, indent=2)
    
    def load_from_disk(self):
        """Load tools and embeddings from disk"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    self.tools = json.load(f)
                self._update_embeddings_matrix()
                logger.info(f"Loaded {len(self.tools)} tools from disk")
            except (json.JSONDecodeError, Exception) as e:
                logger.error(f"Error loading tools from disk: {e}")
                self.tools = []


def get_store(storage_path: str = "tool_embeddings.json"):
    if storage_path not in tools_stores:
        tools_stores[storage_path] = ToolsStore(storage_path)
    return tools_stores[storage_path]
