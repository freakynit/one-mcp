# MCP Tools Documentation

This document describes all available MCP (Model Context Protocol) tools provided by the one-mcp server.

## Overview

The one-mcp server exposes a set of tools through the MCP protocol that allow AI assistants and other MCP clients to manage and search API tools. These tools provide the same functionality as the REST API but through the standardized MCP interface.

## Configuration

To use these tools with an MCP client (like Claude Desktop), add the server to your MCP configuration:

```json
{
  "mcpServers": {
    "one-mcp-server": {
      "command": "python",
      "args": [
        "/absolute/path/to/server.py",
        "--transport", "stdio",
        "--storage_path", "tool_embeddings.json"
      ]
    }
  }
}
```

## Available Tools

### 1. echo_message

**Description**: Echo back the given message (just for testing MCP integration)

**Purpose**: Simple test tool to verify MCP connectivity

**Parameters**:
- `message` (string, required): The message to echo back

**Returns**: The same message that was provided

**Example Usage**:
```python
result = echo_message(message="Hello, MCP!")
# Returns: "Hello, MCP!"
```

**Use Case**: Testing that the MCP server is connected and responding correctly.

---

### 2. search_tool

**Description**: Search for available tools using natural language query

**Purpose**: Find relevant API tools based on semantic similarity

**Parameters**:
- `query` (SearchQuery object, required):
  - `query` (string, required): Natural language search query to find tools
  - `k` (integer, optional): Number of top matching tools to return (default: 5, range: 1-100)

**Returns**: SearchResult object containing:
- `query` (string): The search query that was executed
- `k` (integer): Number of results requested
- `total_results` (integer): Total number of results returned
- `results` (array): Array of matching tools with similarity scores

**Example Usage**:
```python
result = search_tool(
    query=SearchQuery(
        query="how to get user information",
        k=3
    )
)
# Returns top 3 most relevant tools
```

**Example Response**:
```json
{
  "query": "check weather forecast",
  "k": 3,
  "total_results": 1,
  "results": [
    {
      "tool": {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a specific city.",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {"type": "string", "description": "The name of the city to get weather for."},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
          },
          "required": ["city"]
        }
      },
      "similarity_score": 0.78
    }
  ]
}
```

**Use Cases**:
- Finding relevant API endpoints for a specific task
- Discovering what tools are available for a particular domain
- Getting tool recommendations based on natural language descriptions

**Error Handling**: Raises `ValueError` if no tools are available in the store.

---

### 3. delete_tools_by_names

**Description**: Delete specific tools by their names

**Purpose**: Remove tools from the store when they're no longer needed

**Parameters**:
- `delete_input` (DeleteToolsInput object, required):
  - `tool_names` (array of strings, required): Array of tool names to delete

**Returns**: DeleteResult object containing:
- `deleted_count` (integer): Number of tools successfully deleted
- `not_found` (array): List of tool names that were not found
- `remaining_tools` (integer): Number of tools remaining in the store

**Example Usage**:
```python
result = delete_tools_by_names(
    delete_input=DeleteToolsInput(
        tool_names=["get_weather", "convert_currency"]
    )
)
```

**Example Response**:
```json
{
  "deleted_count": 2,
  "not_found": [],
  "remaining_tools": 5
}
```

**Use Cases**:
- Removing deprecated API endpoints
- Cleaning up test data
- Batch deletion of related tools

**Error Handling**: Raises `ValueError` if no tool names are provided.

---

### 4. upload_tools_json

**Description**: Upload tools in JSON format to the store

**Purpose**: Add new API tools to the searchable store

**Parameters**:
- `tools_input` (ToolsInput object, required):
  - `tools` (array of objects, required): Array of OpenAPI-compatible tool definitions

**Tool Object Schema**:
- `name` (string): Tool name/identifier
- `description` (string): Human-readable description of what the tool does
- `method` (string, optional): HTTP method (GET, POST, PUT, DELETE, etc.)
- `path` (string, optional): API endpoint path
- `parameters` (array, optional): List of parameters
- Additional fields as needed

**Returns**: UploadResult object containing:
- `message` (string): Success message describing the upload
- `total_tools` (integer): Total number of tools in the store after upload

**Example Usage**:
```python
result = upload_tools_json(
    tools_input=ToolsInput(
        tools=[
            {
                "type": "function",
                "name": "get_weather",
                "description": "Get the current weather for a specific city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "The name of the city to get weather for."},
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                    },
                    "required": ["city"]
                }
            },
            {
                "type": "function",
                "name": "convert_currency",
                "description": "Convert an amount between two currencies.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number"},
                        "from_currency": {"type": "string"},
                        "to_currency": {"type": "string"}
                    },
                    "required": ["amount", "from_currency", "to_currency"]
                }
            }
        ]
    )
)
```

**Example Response**:
```json
{
  "message": "Successfully added 2 tools",
  "total_tools": 7
}
```

**Use Cases**:
- Adding new API endpoints to the search index
- Bulk importing API specifications
- Populating the tool store with OpenAPI definitions

**Error Handling**: Raises `ValueError` if no tools are provided.

---

### 5. get_stats

**Description**: Get statistics about stored tools

**Purpose**: Retrieve information about the current state of the tool store

**Parameters**: None

**Returns**: StatsResult object containing:
- `total_tools` (integer): Total number of tools in the store
- `storage_path` (string): Absolute path to the storage file
- `model` (string): Name of the embedding model being used

**Example Usage**:
```python
result = get_stats()
```

**Example Response**:
```json
{
  "total_tools": 7,
  "storage_path": "/absolute/path/to/tool_embeddings.json",
  "model": "all-MiniLM-L6-v2"
}
```

**Use Cases**:
- Checking how many tools are currently stored
- Verifying the storage configuration
- Monitoring the embedding model in use

---

### 6. clear_tools

**Description**: Clear all stored tools from the store

**Purpose**: Remove all tools and start fresh

**Parameters**: None

**Returns**: ClearResult object containing:
- `message` (string): Confirmation message that all tools were cleared

**Example Usage**:
```python
result = clear_tools()
```

**Example Response**:
```json
{
  "message": "All tools cleared"
}
```

**Use Cases**:
- Resetting the tool store for testing
- Clearing all data before importing a new set of tools
- Emergency cleanup operations

**⚠️ Warning**: This operation is destructive and cannot be undone. All tools will be permanently removed.

---

## Data Models

### SearchQuery
```python
{
  "query": str,      # Natural language search query
  "k": int = 5       # Number of results (1-100)
}
```

### DeleteToolsInput
```python
{
  "tool_names": List[str]  # Array of tool names to delete
}
```

### ToolsInput
```python
{
  "tools": List[Dict[str, Any]]  # Array of tool definitions
}
```

### SearchResult
```python
{
  "query": str,
  "k": int,
  "total_results": int,
  "results": List[Dict[str, Any]]
}
```

### DeleteResult
```python
{
  "deleted_count": int,
  "not_found": List[str],
  "remaining_tools": int
}
```

### UploadResult
```python
{
  "message": str,
  "total_tools": int
}
```

### StatsResult
```python
{
  "total_tools": int,
  "storage_path": str,
  "model": str
}
```

### ClearResult
```python
{
  "message": str
}
```

---

## Workflow Examples

### Example 1: Adding and Searching Tools

```python
# 1. Add some tools
upload_tools_json(
    tools_input=ToolsInput(
        tools=[
            {"type": "function", "name": "get_weather", "description": "Get the current weather for a specific city."},
            {"type": "function", "name": "get_news_headlines", "description": "Fetch the latest news headlines for a given topic."},
            {"type": "function", "name": "convert_currency", "description": "Convert an amount between two currencies."}
        ]
    )
)

# 2. Search for weather-related tools
results = search_tool(
    query=SearchQuery(query="check weather forecast", k=5)
)

# 3. Check statistics
stats = get_stats()
```

### Example 2: Managing Tools

```python
# 1. Get current statistics
stats = get_stats()
print(f"Current tools: {stats.total_tools}")

# 2. Delete specific tools
delete_result = delete_tools_by_names(
    delete_input=DeleteToolsInput(
        tool_names=["convert_currency", "get_news_headlines"]
    )
)
print(f"Deleted: {delete_result.deleted_count}")

# 3. Clear everything if needed
clear_tools()
```

### Example 3: Tool Discovery

```python
# Upload a comprehensive set of tools
upload_tools_json(
    tools_input=ToolsInput(
        tools=[
            {
                "type": "function",
                "name": "get_weather",
                "description": "Get the current weather for a specific city.",
                "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}
            },
            {
                "type": "function",
                "name": "get_flight_status",
                "description": "Retrieve the live status of a flight.",
                "parameters": {"type": "object", "properties": {"flight_number": {"type": "string"}}}
            },
            {
                "type": "function",
                "name": "find_restaurant",
                "description": "Find restaurants in a city that match a cuisine type.",
                "parameters": {"type": "object", "properties": {"city": {"type": "string"}, "cuisine": {"type": "string"}}}
            }
        ]
    )
)

# Search using natural language
weather_tools = search_tool(
    query=SearchQuery(query="get weather forecast", k=2)
)

travel_tools = search_tool(
    query=SearchQuery(query="check flight information", k=2)
)
```

---

## Technical Details

### Embedding Model

The tools use **all-MiniLM-L6-v2** from sentence-transformers for generating embeddings. This model:
- Produces 384-dimensional embeddings
- Is optimized for semantic similarity tasks
- Provides good performance with minimal resource usage

### Similarity Scoring

- Uses cosine similarity to compare query embeddings with tool embeddings
- Scores range from 0 (no similarity) to 1 (identical)
- Tools are ranked by similarity score in descending order

### Persistence

- Tools and embeddings are automatically saved to disk
- Default storage file: `tool_embeddings.json`
- Loaded automatically on server startup
- Updated after every modification operation

### Tool Serialization

Tools are serialized with priority given to `name` and `description` fields:
```
Format: "Name: {name} | Description: {description} | {other_fields_as_json}"
```

This ensures that the most semantically relevant fields are weighted appropriately in the embeddings.

---

## Best Practices

1. **Descriptive Tool Names**: Use clear, descriptive names for better search results
2. **Detailed Descriptions**: Provide comprehensive descriptions including use cases and parameters
3. **Consistent Schema**: Maintain consistent field structure across tools
4. **Regular Cleanup**: Periodically remove deprecated or unused tools
5. **Batch Operations**: Use batch uploads for adding multiple tools at once
6. **Test Queries**: Verify search quality with diverse natural language queries

---

## Troubleshooting

### No Results Returned

- Check if tools are loaded: use `get_stats()`
- Verify tool descriptions are detailed enough
- Try different search query phrasings
- Ensure tools were uploaded successfully

### Poor Search Quality

- Add more descriptive tool descriptions
- Include relevant keywords in descriptions
- Use more specific search queries
- Consider the semantic meaning, not just keywords

### Tools Not Persisting

- Verify storage path permissions
- Check that `storage_path` is writable
- Review server logs for errors

---

## Integration Examples

### Using with Claude Desktop

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "one-mcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/server.py",
        "--transport", "stdio"
      ]
    }
  }
}
```

Then in Claude Desktop, you can use natural language:
- "Search for tools related to weather information"
- "Upload these API tools: [tool definitions from test_specs.json]"
- "Delete the currency conversion tool"
- "Show me statistics about available tools"

---

## Additional Resources

- [REST API Documentation](./CURLS.md)
- [Project README](./README.md)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
