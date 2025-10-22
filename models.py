from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ToolsInput(BaseModel):
    tools: List[Dict[str, Any]] = Field(
        ..., 
        description="Array of OpenAPI compatible tools"
    )


class SearchQuery(BaseModel):
    query: str = Field(..., description="Natural language search query to search for available tools")
    k: Optional[int] = Field(
        5, 
        description="Number of top matching tools to return", 
        ge=1, 
        le=100
    )


class DeleteToolsInput(BaseModel):
    tool_names: List[str] = Field(
        ..., 
        description="Array of tool names to delete"
    )


class SearchResult(BaseModel):
    query: str = Field(..., description="The search query that was executed")
    k: int = Field(..., description="Number of results requested")
    total_results: int = Field(..., description="Total number of results returned")
    results: List[Dict[str, Any]] = Field(..., description="Array of matching tools with similarity scores")


class DeleteResult(BaseModel):
    deleted_count: int = Field(..., description="Number of tools successfully deleted")
    not_found: List[str] = Field(..., description="List of tool names that were not found")
    remaining_tools: int = Field(..., description="Number of tools remaining in the store")


class UploadResult(BaseModel):
    message: str = Field(..., description="Success message describing the upload")
    total_tools: int = Field(..., description="Total number of tools in the store after upload")


class StatsResult(BaseModel):
    total_tools: int = Field(..., description="Total number of tools in the store")
    storage_path: str = Field(..., description="Absolute path to the storage file")
    model: str = Field(..., description="Name of the embedding model being used")


class ClearResult(BaseModel):
    message: str = Field(..., description="Confirmation message that all tools were cleared")
