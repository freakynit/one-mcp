from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json
from models import SpecsInput, SearchQuery
from spec_store import SpecStore

# Initialize storage
store = SpecStore()


def create_app(mcp):
    """Create and configure the FastAPI application"""
    api = FastAPI(title="API Tools with MCP", version="1.0.0")

    # Basic status endpoint
    @api.get("/api/status")
    def status():
        return {"status": "ok", "total_specs": len(store.specs)}


    # Spec post endpoint to upload specs in JSON format
    @api.post("/api/specs/upload-json")
    async def upload_specs_json(specs_input: SpecsInput):
        specs = specs_input.specs
        if not specs:
            raise HTTPException(status_code=400, detail="No specs provided")
        initial_count = len(store.specs)
        store.add_specs(specs)
        return {
            "message": f"Successfully added {len(store.specs) - initial_count} specs",
            "total_specs": len(store.specs)
        }


    # Spec upload endpoint to upload specs in file format
    @api.post("/api/specs/upload-file")
    async def upload_specs_file(file: UploadFile = File(...)):
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="Only .json files are supported")
        try:
            content = await file.read()
            data = json.loads(content)
            specs = data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON file")

        if not specs:
            raise HTTPException(status_code=400, detail="No specs provided")

        initial_count = len(store.specs)
        store.add_specs(specs)
        return {
            "message": f"Successfully added {len(store.specs) - initial_count} specs",
            "total_specs": len(store.specs)
        }


    # Spec search endpoint
    @api.post("/api/specs/search")
    async def search_specs(query: SearchQuery):
        """
        Search for similar OpenAPI specs using natural language query.
        Returns top k most similar specs based on cosine similarity.
        """
        if not store.specs:
            return JSONResponse(
                content={
                    "message": "No specs available. Please upload specs first.", 
                    "results": []
                },
                status_code=200
            )
        
        results = store.search(query.query, query.k)
        
        return {
            "query": query.query,
            "k": query.k,
            "total_results": len(results),
            "results": results
        }

    # Get stats endpoint
    @api.get("/api/specs/stats")
    async def get_stats():
        """Get statistics about stored specs"""
        return {
            "total_specs": len(store.specs),
            "storage_path": str(store.storage_path.absolute()),
            "model": store.model_name
        }

    # Clear specs endpoint
    @api.delete("/api/specs/clear")
    async def clear_specs():
        """Clear all stored specs"""
        store.specs = []
        store.embeddings = None
        store.save_to_disk()
        return {"message": "All specs cleared"}

    # Mount MCP at /mcp
    api.mount("/mcp", mcp.http_app())
    
    return api
