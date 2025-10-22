### 1. Check Server Status
```bash
curl http://localhost:8003/api/status
```

### 2. Upload Tools (JSON Body)
```bash
curl -X POST http://localhost:8003/api/tools/upload-json \
  -H "Content-Type: application/json" \
  -d '{
    "tools": [
      { "name": "getUserProfile", "description": "Retrieves user profile information including email and preferences", "method": "GET", "path": "/api/v1/users/{userId}", "parameters": ["userId"] },
      { "name": "createOrder", "description": "Creates a new order for purchasing products", "method": "POST", "path": "/api/v1/orders", "requestBody": {"items": "array", "total": "number"} },
      { "name": "updateUserSettings", "description": "Updates user notification and privacy settings", "method": "PUT", "path": "/api/v1/users/{userId}/settings", "parameters": ["userId"] }
    ]
  }'
```

### 3. Upload Tools (File Upload)
First create a test file:
```bash
echo '[
  {
    "name": "listProducts",
    "description": "Lists all available products with pagination",
    "method": "GET",
    "path": "/api/v1/products"
  }
]' > test_tools.json
```

Then upload it:
```bash
curl -X POST http://localhost:8003/api/tools/upload-file \
  -F "file=@test_tools.json;type=application/json"
```

### 4. Search for Similar Tools
```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how to get user information",
    "k": 3
  }'
```

```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "create new purchase",
    "k": 2
  }'
```

```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "change settings and preferences",
    "k": 5
  }'
```

### 5. Get Statistics
```bash
curl http://localhost:8003/api/tools/stats
```

### 6. Clear All Tools
```bash
curl -X DELETE http://localhost:8003/api/tools/clear
```

### 7. Delete Specific Tools
```bash
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{
    "tool_names": ["getUserProfile", "createOrder"]
  }'
```

### 8. Delete Multiple Tools (Batch Deletion)
```bash
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{
    "tool_names": ["getUserProfile", "createOrder", "updateUserSettings", "listProducts"]
  }'
```

### 9. Test MCP Endpoint (HTTP Straming Mode)
```bash
curl http://localhost:8003/mcp
```

### Complete Testing Workflow
```bash
# Start fresh
curl -X DELETE http://localhost:8003/api/tools/clear

# Check initial stats
curl http://localhost:8003/api/status

# Upload some tools
curl -X POST http://localhost:8003/api/tools/upload-json \
  -H "Content-Type: application/json" \
  -d '{"tools": [{"name": "login", "description": "User authentication endpoint"}, {"name": "logout", "description": "End user session"}, {"name": "register", "description": "User registration endpoint"}]}'

# Search for authentication related
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{"query": "authenticate user", "k": 5}'

# Delete specific tools
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{"tool_names": ["register"]}'

# Check final stats
curl http://localhost:8003/api/tools/stats
```

### Testing with Pretty Output (using jq)
```bash
curl -s http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{"query": "user profile", "k": 3}' | jq '.'
```

All endpoints return JSON responses. The search endpoint will show similarity scores between 0 and 1, where higher scores indicate better matches to your query.
