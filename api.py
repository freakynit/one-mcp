from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json
from models import ToolsInput, SearchQuery, DeleteToolsInput
from tools_store import get_store


def create_app(mcp, storage_path: str = "tool_embeddings.json"):
    """Create and configure the FastAPI application"""
    api = FastAPI(title="API Tools with MCP", version="1.0.0")

    store_instance = get_store(storage_path)

    # Basic status endpoint
    @api.get("/api/status")
    def status():
        return {"status": "ok", "total_tools": len(store_instance.tools)}


    # Tool post endpoint to upload tools in JSON format
    @api.post("/api/tools/upload-json")
    async def upload_tools_json(tools_input: ToolsInput):
        tools = tools_input.tools
        if not tools:
            raise HTTPException(status_code=400, detail="No tools provided")
        initial_count = len(store_instance.tools)
        store_instance.add_tools(tools)
        return {
            "message": f"Successfully added {len(store_instance.tools) - initial_count} tools",
            "total_tools": len(store_instance.tools)
        }


    # Tool upload endpoint to upload tools in file format
    @api.post("/api/tools/upload-file")
    async def upload_tools_file(file: UploadFile = File(...)):
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="Only .json files are supported")
        try:
            content = await file.read()
            data = json.loads(content)
            tools = data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON file")

        if not tools:
            raise HTTPException(status_code=400, detail="No tools provided")

        initial_count = len(store_instance.tools)
        store_instance.add_tools(tools)
        return {
            "message": f"Successfully added {len(store_instance.tools) - initial_count} tools",
            "total_tools": len(store_instance.tools)
        }


    # Tool search endpoint
    @api.post("/api/tools/search")
    async def search_tools(query: SearchQuery):
        """
        Search for similar OpenAPI tools using natural language query.
        Returns top k most similar tools based on cosine similarity.
        """
        if not store_instance.tools:
            return JSONResponse(
                content={
                    "message": "No tools available. Please upload tools first.", 
                    "results": []
                },
                status_code=200
            )
        
        results = store_instance.search(query.query, query.k)
        
        return {
            "query": query.query,
            "k": query.k,
            "total_results": len(results),
            "results": results
        }

    # Get stats endpoint
    @api.get("/api/tools/stats")
    async def get_stats():
        """Get statistics about stored tools"""
        return {
            "total_tools": len(store_instance.tools),
            "storage_path": str(store_instance.storage_path.absolute()),
            "model": store_instance.model_name
        }

    # Clear tools endpoint
    @api.delete("/api/tools/clear")
    async def clear_tools():
        """Clear all stored tools"""
        store_instance.tools = []
        store_instance.embeddings = None
        store_instance.save_to_disk()
        return {"message": "All tools cleared"}

    # Delete specific tools endpoint
    @api.delete("/api/tools/delete")
    async def delete_tools(delete_input: DeleteToolsInput):
        """Delete specific tools by their names"""
        if not delete_input.tool_names:
            raise HTTPException(status_code=400, detail="No tool names provided")
        
        result = store_instance.delete_tools(delete_input.tool_names)
        
        if result["deleted_count"] == 0 and result["not_found"]:
            return JSONResponse(
                content=result,
                status_code=404
            )
        
        return result

    # Mount MCP at /mcp
    api.mount("/mcp", mcp.http_app())
    
    return api
