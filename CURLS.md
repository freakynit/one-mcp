# API Testing Guide with cURL

This document provides comprehensive examples for testing all REST API endpoints.

## Prerequisites

Ensure the server is running in HTTP mode:

```bash
python server.py --transport http --port 8003
```

Or in dual transport mode:

```bash
python server.py --transport stdio,http --port 8003
```

---

## API Endpoints

### 1. Check Server Status

**Endpoint**: `GET /api/status`

**Description**: Returns server health status and total tool count.

```bash
curl http://localhost:8003/api/status
```

**Response**:
```json
{
  "status": "ok",
  "total_tools": 0
}
```

---

### 2. Upload Tools (JSON Body)

**Endpoint**: `POST /api/tools/upload-json`

**Description**: Upload tools as JSON in request body.

```bash
curl -X POST http://localhost:8003/api/tools/upload-json \
  -H "Content-Type: application/json" \
  -d '{
    "tools": [
      { "type": "function", "name": "get_weather", "description": "Get the current weather for a specific city.", "parameters": {"type": "object", "properties": {"city": {"type": "string", "description": "The name of the city to get weather for."}, "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Temperature unit to return results in."}}, "required": ["city"]} },
      { "type": "function", "name": "get_news_headlines", "description": "Fetch the latest news headlines for a given topic.", "parameters": {"type": "object", "properties": {"topic": {"type": "string", "description": "The topic to get headlines for, e.g. technology, sports, health."}, "limit": {"type": "integer", "description": "Number of headlines to return."}}, "required": ["topic"]} },
      { "type": "function", "name": "convert_currency", "description": "Convert an amount between two currencies.", "parameters": {"type": "object", "properties": {"amount": {"type": "number", "description": "Amount of money to convert."}, "from_currency": {"type": "string", "description": "The source currency code, e.g. USD."}, "to_currency": {"type": "string", "description": "The target currency code, e.g. EUR."}}, "required": ["amount", "from_currency", "to_currency"]} }
    ]
  }'
```

**Response**:
```json
{
  "message": "Successfully added 3 tools",
  "total_tools": 3
}
```

---

### 3. Upload Tools (File Upload)

**Endpoint**: `POST /api/tools/upload-file`

**Description**: Upload tools from a JSON file.

First create a test file (or use the provided `test_specs.json`):
```bash
echo '[
  {
    "type": "function",
    "name": "get_flight_status",
    "description": "Retrieve the live status of a flight.",
    "parameters": {
      "type": "object",
      "properties": {
        "flight_number": {"type": "string", "description": "The airline flight number, e.g. AA100 or LH760."},
        "date": {"type": "string", "description": "Date of the flight in YYYY-MM-DD format."}
      },
      "required": ["flight_number"]
    }
  }
]' > test_tools.json
```

Then upload it:
```bash
curl -X POST http://localhost:8003/api/tools/upload-file \
  -F "file=@test_tools.json;type=application/json"
```

**Response**:
```json
{
  "message": "Successfully added 1 tools",
  "total_tools": 4
}
```

**Or upload the sample file directly**:
```bash
curl -X POST http://localhost:8003/api/tools/upload-file \
  -F "file=@test_specs.json;type=application/json"
```

---

### 4. Search for Similar Tools

**Endpoint**: `POST /api/tools/search`

**Description**: Search for tools using semantic similarity with natural language queries.

**Example 1**: Find weather-related tools
```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "check weather forecast",
    "k": 3
  }'
```

**Example 2**: Find currency conversion tools
```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "convert money between currencies",
    "k": 2
  }'
```

**Example 3**: Find news-related tools
```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "latest headlines and news",
    "k": 5
  }'
```

**Sample Response**:
```json
{
    "query": "check weather forecast",
    "k": 3,
    "total_results": 3,
    "results": [{
        "tool": {
            "type": "function",
            "name": "get_weather",
            "description": "Get the current weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for."
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit to return results in."
                    }
                },
                "required": ["city"]
            }
        },
        "similarity_score": 0.4655591985594944
    }, {
        "tool": {
            "type": "function",
            "name": "get_news_headlines",
            "description": "Fetch the latest news headlines for a given topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to get headlines for, e.g. technology, sports, health."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of headlines to return."
                    }
                },
                "required": ["topic"]
            }
        },
        "similarity_score": 0.14447337962809007
    }, {
        "tool": {
            "name": "updateUserSettings",
            "description": "Updates user notification and privacy settings",
            "method": "PUT",
            "path": "/api/v1/users/{userId}/settings",
            "parameters": ["userId"]
        },
        "similarity_score": 0.08695475063777121
    }]
}
```

---

### 5. Get Statistics

**Endpoint**: `GET /api/tools/stats`

**Description**: Get statistics about stored tools including count, storage path, and model.

```bash
curl http://localhost:8003/api/tools/stats
```

**Response**:
```json
{
  "total_tools": 4,
  "storage_path": "/absolute/path/to/tool_embeddings.json",
  "model": "all-MiniLM-L6-v2"
}
```

---

### 6. Clear All Tools

**Endpoint**: `DELETE /api/tools/clear`

**Description**: Remove all stored tools and their embeddings.

```bash
curl -X DELETE http://localhost:8003/api/tools/clear
```

**Response**:
```json
{
  "message": "All tools cleared"
}
```

---

### 7. Delete Specific Tools

**Endpoint**: `DELETE /api/tools/delete`

**Description**: Delete specific tools by their names.

```bash
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{
    "tool_names": ["get_weather", "get_news_headlines"]
  }'
```

**Response**:
```json
{
  "deleted_count": 2,
  "not_found": [],
  "remaining_tools": 2
}
```

---

### 8. Delete Multiple Tools (Batch Deletion)

**Endpoint**: `DELETE /api/tools/delete`

**Description**: Delete multiple tools at once.

```bash
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{
    "tool_names": ["get_weather", "get_news_headlines", "convert_currency", "get_flight_status"]
  }'
```

**Response**:
```json
{
  "deleted_count": 4,
  "not_found": [],
  "remaining_tools": 0
}
```

---

### 9. Test MCP Endpoint (HTTP Streaming Mode)

**Endpoint**: `GET /mcp`

**Description**: Access the MCP HTTP endpoint.

```bash
curl http://localhost:8003/mcp
```

---

## Complete Testing Workflow

Here's a complete workflow to test all functionality:

```bash
# 1. Start fresh
curl -X DELETE http://localhost:8003/api/tools/clear

# 2. Check initial stats
curl http://localhost:8003/api/status

# 3. Upload some tools
curl -X POST http://localhost:8003/api/tools/upload-json \
  -H "Content-Type: application/json" \
  -d '{"tools": [
    {"type": "function", "name": "get_weather", "description": "Get the current weather for a specific city."},
    {"type": "function", "name": "convert_currency", "description": "Convert an amount between two currencies."},
    {"type": "function", "name": "get_news_headlines", "description": "Fetch the latest news headlines for a given topic."}
  ]}'

# 4. Search for authentication related tools
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{"query": "weather information", "k": 5}'

# 5. Get detailed statistics
curl http://localhost:8003/api/tools/stats

# 6. Delete specific tools
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{"tool_names": ["convert_currency"]}'

# 7. Check final stats
curl http://localhost:8003/api/tools/stats
```

---

## Testing with Pretty Output (using jq)

For formatted JSON output, pipe results through `jq`:

```bash
# Pretty print search results
curl -s http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{"query": "get weather forecast", "k": 3}' | jq '.'

# Pretty print stats
curl -s http://localhost:8003/api/tools/stats | jq '.'
```

---

## Response Format Notes

- All endpoints return JSON responses with appropriate HTTP status codes
- Search results include similarity scores between 0 and 1 (higher = better match)
- Error responses include descriptive error messages
- Upload endpoints return the new total tool count
- Delete endpoints return counts of deleted/not-found tools
