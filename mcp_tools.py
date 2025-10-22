from fastmcp import FastMCP
from models import ToolsInput, SearchQuery, DeleteToolsInput, SearchResult, DeleteResult, UploadResult, StatsResult, ClearResult
from tools_store import get_store

# Create MCP server
mcp = FastMCP("API Tools")

# Get the default store instance
store = get_store()


@mcp.tool
def echo_message(message: str) -> str:
    """Echo back the given message"""
    return message


@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b


@mcp.tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integer numbers together."""
    return a * b

@mcp.tool
async def search_tool(query: SearchQuery) -> SearchResult:
        """
        Search for available tools using natural language query.
        Returns top k most similar tools based on cosine similarity.
        """
        if not store.tools:
            raise ValueError("No tools available. Please upload/add tools first.")
        
        results = store.search(query.query, query.k)
        
        return SearchResult(
            query=query.query,
            k=query.k,
            total_results=len(results),
            results=results
        )

@mcp.tool
async def delete_tools_by_names(delete_input: DeleteToolsInput) -> DeleteResult:
        """
        Delete specific tools by their names.
        Returns information about deleted tools and any tools that were not found.
        """
        if not delete_input.tool_names:
            raise ValueError("No tool names provided for deletion.")
        
        result = store.delete_tools(delete_input.tool_names)
        return DeleteResult(
             deleted_count=result["deleted_count"],
             not_found=result["not_found"],
             remaining_tools=result["remaining_tools"]
         )

@mcp.tool
async def upload_tools_json(tools_input: ToolsInput) -> UploadResult:
        """
        Upload tools in JSON format to the store.
        Returns information about the upload operation.
        """
        tools = tools_input.tools
        if not tools:
            raise ValueError("No tools provided")
        
        initial_count = len(store.tools)
        store.add_tools(tools)
        added_count = len(store.tools) - initial_count
        
        return UploadResult(
             message=f"Successfully added {added_count} tools",
             total_tools=len(store.tools)
         )

@mcp.tool
async def get_stats() -> StatsResult:
        """
        Get statistics about stored tools.
        Returns information about the current state of the tool store.
        """
        return StatsResult(
             total_tools=len(store.tools),
             storage_path=str(store.storage_path.absolute()),
             model=store.model_name
         )

@mcp.tool
async def clear_tools() -> ClearResult:
        """
        Clear all stored tools from the store.
        Returns confirmation that all tools have been cleared.
        """
        store.tools = []
        store.embeddings = None
        store.save_to_disk()
        return ClearResult(message="All tools cleared")