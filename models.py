from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class SpecsInput(BaseModel):
    specs: List[Dict[str, Any]] = Field(
        ..., 
        description="Array of OpenAPI compatible specs"
    )


class SearchQuery(BaseModel):
    query: str = Field(..., description="Natural language search query to search for available tools")
    k: Optional[int] = Field(
        5, 
        description="Number of top matching tools to return", 
        ge=1, 
        le=100
    )
