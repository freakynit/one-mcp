### 1. Check Server Status
```bash
curl http://localhost:8003/api/status
```

### 2. Upload Specs (JSON Body)
```bash
curl -X POST http://localhost:8003/api/specs/upload-json \
  -H "Content-Type: application/json" \
  -d '{
    "specs": [
      { "name": "getUserProfile", "description": "Retrieves user profile information including email and preferences", "method": "GET", "path": "/api/v1/users/{userId}", "parameters": ["userId"] },
      { "name": "createOrder", "description": "Creates a new order for purchasing products", "method": "POST", "path": "/api/v1/orders", "requestBody": {"items": "array", "total": "number"} },
      { "name": "updateUserSettings", "description": "Updates user notification and privacy settings", "method": "PUT", "path": "/api/v1/users/{userId}/settings", "parameters": ["userId"] }
    ]
  }'
```

### 3. Upload Specs (File Upload)
First create a test file:
```bash
echo '[
  {
    "name": "listProducts",
    "description": "Lists all available products with pagination",
    "method": "GET",
    "path": "/api/v1/products"
  }
]' > test_specs.json
```

Then upload it:
```bash
curl -X POST http://localhost:8003/api/specs/upload-file \
  -F "file=@test_specs.json;type=application/json"
```

### 4. Search for Similar Specs
```bash
curl -X POST http://localhost:8003/api/specs/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how to get user information",
    "k": 3
  }'
```

```bash
curl -X POST http://localhost:8003/api/specs/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "create new purchase",
    "k": 2
  }'
```

```bash
curl -X POST http://localhost:8003/api/specs/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "change settings and preferences",
    "k": 5
  }'
```

### 5. Get Statistics
```bash
curl http://localhost:8003/api/specs/stats
```

### 6. Clear All Specs
```bash
curl -X DELETE http://localhost:8003/api/specs/clear
```

### 7. Test MCP Endpoint (HTTP Straming Mode)
```bash
curl http://localhost:8003/mcp
```

### Complete Testing Workflow
```bash
# Start fresh
curl -X DELETE http://localhost:8003/api/specs/clear

# Check initial stats
curl http://localhost:8003/api/stats

# Upload some specs
curl -X POST http://localhost:8003/api/specs/upload \
  -H "Content-Type: application/json" \
  -d '{"specs": [{"name": "login", "description": "User authentication endpoint"}, {"name": "logout", "description": "End user session"}]}'

# Search for authentication related
curl -X POST http://localhost:8003/api/specs/search \
  -H "Content-Type: application/json" \
  -d '{"query": "authenticate user", "k": 5}'

# Check final stats
curl http://localhost:8003/api/specs/stats
```

### Testing with Pretty Output (using jq)
```bash
curl -s http://localhost:8003/api/specs/search \
  -H "Content-Type: application/json" \
  -d '{"query": "user profile", "k": 3}' | jq '.'
```

All endpoints return JSON responses. The search endpoint will show similarity scores between 0 and 1, where higher scores indicate better matches to your query.
