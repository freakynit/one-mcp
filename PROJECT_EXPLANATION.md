# Project Explanation: one-mcp

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Technical Stack](#technical-stack)
5. [Key Features](#key-features)
6. [How It Works](#how-it-works)
7. [API Endpoints](#api-endpoints)
8. [MCP Tools](#mcp-tools)
9. [Data Flow](#data-flow)
10. [Deployment](#deployment)
11. [Use Cases](#use-cases)

---

## Project Overview

**one-mcp** is an intelligent tool management server that implements the Model Context Protocol (MCP). It enables users to upload, store, manage, and semantically search API tools using natural language queries. The project leverages modern machine learning techniques (sentence embeddings) to provide intelligent tool discovery.

### What Problem Does It Solve?

In modern software development, teams often work with hundreds or thousands of API endpoints across multiple services. Finding the right API tool for a specific task can be challenging when you have to search through extensive documentation. **one-mcp** solves this by:

1. **Semantic Search**: Instead of exact string matching, it understands the intent behind queries like "how to get user information" and returns relevant tools like `getUserProfile`
2. **Centralized Tool Management**: Provides a single location to store and manage API tool definitions
3. **MCP Integration**: Enables AI assistants and other MCP-compatible clients to discover and use tools programmatically

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     one-mcp Server                          │
│                                                             │
│  ┌─────────────────┐         ┌──────────────────┐         │
│  │   FastAPI App   │◄────────┤  MCP Server      │         │
│  │   (HTTP API)    │         │  (stdio/http)    │         │
│  └────────┬────────┘         └─────────┬────────┘         │
│           │                             │                   │
│           │         ┌──────────────────▼────────┐          │
│           └────────►│   Tools Store             │          │
│                     │  - In-memory storage      │          │
│                     │  - Disk persistence       │          │
│                     │  - Embedding management   │          │
│                     └──────────┬────────────────┘          │
│                                │                            │
│                     ┌──────────▼────────────────┐          │
│                     │ Sentence Transformer      │          │
│                     │ (all-MiniLM-L6-v2)       │          │
│                     │ - Generate embeddings     │          │
│                     │ - Semantic similarity     │          │
│                     └───────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
User Request → FastAPI/MCP → Tools Store → Sentence Transformer → Cosine Similarity → Results
```

---

## Core Components

### 1. `app.py` - Application Entry Point

**Purpose**: Server initialization, configuration, and transport management

**Key Classes**:
- `ServerConfig`: Manages server configuration (transport, port, host, storage path)
- `MCPServer`: Main server class that handles both HTTP and stdio transports

**Key Features**:
- Multi-transport support (stdio, HTTP, or both simultaneously)
- Graceful shutdown handling with signal handlers
- Thread-based HTTP server management for dual-mode operation
- Command-line argument parsing for flexible deployment

**Transport Modes**:
1. **stdio only**: For direct MCP client integration
2. **http only**: For web-based API access
3. **dual mode**: Runs both transports simultaneously (HTTP in background thread, stdio in main thread)

**Example Usage**:
```bash
python app.py --transport stdio,http --port 8003 --storage_path tool_embeddings.json
```

### 2. `api.py` - REST API Routes

**Purpose**: Defines all HTTP endpoints for tool management

**Endpoints Overview**:
- `GET /api/status`: Health check and tool count
- `POST /api/tools/upload-json`: Upload tools via JSON body
- `POST /api/tools/upload-file`: Upload tools via file upload
- `POST /api/tools/search`: Semantic search for tools
- `GET /api/tools/stats`: Get statistics about stored tools
- `DELETE /api/tools/clear`: Clear all tools
- `DELETE /api/tools/delete`: Delete specific tools by name

**Integration**:
- Mounts the MCP server at `/mcp` endpoint
- Uses Pydantic models for request/response validation
- Integrates with shared `ToolsStore` instance

### 3. `mcp_tools.py` - MCP Tool Definitions

**Purpose**: Defines MCP-compatible tools that can be called by MCP clients

**Available MCP Tools**:
1. `echo_message`: Simple echo tool for testing
2. `add`: Mathematical addition
3. `multiply`: Mathematical multiplication
4. `search_tool`: Semantic search for tools
5. `delete_tools_by_names`: Delete tools by name
6. `upload_tools_json`: Upload new tools
7. `get_stats`: Get tool statistics
8. `clear_tools`: Clear all tools

**MCP Integration**:
- Uses `fastmcp` library to create MCP server
- Tools are decorated with `@mcp.tool`
- Returns structured Pydantic models for type safety

### 4. `models.py` - Data Models

**Purpose**: Defines Pydantic models for request/response validation and documentation

**Model Categories**:

**Input Models**:
- `ToolsInput`: For uploading tools
- `SearchQuery`: For search requests
- `DeleteToolsInput`: For deletion requests

**Output Models**:
- `SearchResult`: Search results with similarity scores
- `DeleteResult`: Deletion operation results
- `UploadResult`: Upload operation results
- `StatsResult`: Statistics about the store
- `ClearResult`: Confirmation of clear operation

**Benefits**:
- Type safety and validation
- Automatic API documentation
- Clear data contracts

### 5. `tools_store.py` - Storage and Embedding Management

**Purpose**: Core data management with ML-powered semantic search

**Key Class: `ToolsStore`**

**Responsibilities**:
1. **Tool Storage**: In-memory storage with disk persistence
2. **Embedding Generation**: Converts tools to vector embeddings
3. **Semantic Search**: Cosine similarity-based tool retrieval
4. **CRUD Operations**: Add, delete, and clear tools
5. **Persistence**: JSON-based disk storage

**Key Methods**:

```python
add_tools(tools)           # Add tools and generate embeddings
search(query, k)           # Semantic search with top-k results
delete_tools(tool_names)   # Delete specific tools
save_to_disk()            # Persist to JSON
load_from_disk()          # Load from JSON
_serialize_tool(tool)     # Convert tool to searchable text
```

**Embedding Strategy**:
- Uses `sentence-transformers` with `all-MiniLM-L6-v2` model
- Prioritizes tool name and description for embeddings
- Stores embeddings as lists in JSON for persistence
- Maintains numpy array for efficient similarity computation

**Search Algorithm**:
1. Encode user query as embedding vector
2. Calculate cosine similarity with all tool embeddings
3. Sort by similarity score (descending)
4. Return top-k results with scores

---

## Technical Stack

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework for HTTP API | >=0.104.0 |
| **fastmcp** | Model Context Protocol implementation | >=0.2.0 |
| **sentence-transformers** | Text embedding generation | >=2.2.0 |
| **PyTorch** | Deep learning backend | 2.4.1 |
| **scikit-learn** | Cosine similarity computation | >=1.3.0 |
| **Pydantic** | Data validation and serialization | (via FastAPI) |
| **uvicorn** | ASGI server | >=0.24.0 |

### Machine Learning Model

**Model**: `all-MiniLM-L6-v2`
- **Type**: Sentence transformer
- **Dimension**: 384-dimensional embeddings
- **Size**: ~22MB (small and efficient)
- **Performance**: Fast inference on CPU
- **Quality**: Good balance between speed and accuracy

---

## Key Features

### 1. Semantic Search

**How it works**:
```python
# User query: "how to get user information"
# System finds: getUserProfile (high similarity)
#               updateUserSettings (medium similarity)
```

**Advantages**:
- Natural language understanding
- Fuzzy matching (handles typos and variations)
- Context-aware results
- No need for exact keyword matching

### 2. Dual Transport Support

**stdio Transport**:
- Direct integration with MCP clients
- Uses standard input/output for communication
- Ideal for local AI assistants (Claude Desktop, etc.)

**HTTP Transport**:
- RESTful API for web integration
- cURL-friendly for testing
- Supports browser-based clients

**Dual Mode**:
- Runs both transports simultaneously
- HTTP server in background thread
- stdio in main thread
- Useful for development and testing

### 3. Persistent Storage

**Storage Format**:
```json
[
  {
    "original": {
      "name": "getUserProfile",
      "description": "Retrieves user profile",
      "method": "GET",
      "path": "/api/v1/users/{userId}"
    },
    "embedding": [0.123, -0.456, 0.789, ...]
  }
]
```

**Benefits**:
- Tools persist across server restarts
- Embeddings cached for fast startup
- Human-readable JSON format
- Easy backup and migration

### 4. Tool Serialization Strategy

**Prioritization**:
1. Tool name (highest weight)
2. Tool description
3. Additional metadata (method, path, parameters)

**Example Serialization**:
```
Input:  {"name": "getUserProfile", "description": "Get user info", "method": "GET"}
Output: "Name: getUserProfile | Description: Get user info | {\"method\": \"GET\"}"
```

This ensures that name and description have maximum impact on search relevance.

---

## How It Works

### Tool Upload Flow

```
1. User uploads tool(s) via API or MCP
   ↓
2. ToolsStore receives tool definitions
   ↓
3. For each tool:
   a. Serialize to text (name + description + metadata)
   b. Generate embedding using sentence transformer
   c. Store {original: tool, embedding: vector}
   ↓
4. Update in-memory embeddings matrix
   ↓
5. Save to disk (tool_embeddings.json)
   ↓
6. Return success with count
```

### Search Flow

```
1. User submits natural language query
   ↓
2. Query converted to embedding vector
   ↓
3. Compute cosine similarity with all tool embeddings
   ↓
4. Sort by similarity (high to low)
   ↓
5. Return top-k results with scores
   ↓
6. Each result includes:
   - Original tool definition
   - Similarity score (0.0 to 1.0)
```

### Similarity Score Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 0.8 - 1.0 | Highly relevant |
| 0.6 - 0.8 | Relevant |
| 0.4 - 0.6 | Somewhat relevant |
| < 0.4 | Low relevance |

---

## API Endpoints

### 1. Status Check
```bash
GET /api/status
```
**Response**:
```json
{
  "status": "ok",
  "total_tools": 42
}
```

### 2. Upload Tools (JSON)
```bash
POST /api/tools/upload-json
Content-Type: application/json
```
**Request Body**:
```json
{
  "tools": [
    {
      "name": "getUserProfile",
      "description": "Retrieves user profile information",
      "method": "GET",
      "path": "/api/v1/users/{userId}",
      "parameters": ["userId"]
    }
  ]
}
```

### 3. Upload Tools (File)
```bash
POST /api/tools/upload-file
Content-Type: multipart/form-data
```
Accepts `.json` files containing tool arrays.

### 4. Search Tools
```bash
POST /api/tools/search
Content-Type: application/json
```
**Request**:
```json
{
  "query": "how to get user information",
  "k": 5
}
```

**Response**:
```json
{
  "query": "how to get user information",
  "k": 5,
  "total_results": 3,
  "results": [
    {
      "tool": {
        "name": "getUserProfile",
        "description": "Retrieves user profile information",
        "method": "GET",
        "path": "/api/v1/users/{userId}"
      },
      "similarity_score": 0.87
    }
  ]
}
```

### 5. Get Statistics
```bash
GET /api/tools/stats
```
**Response**:
```json
{
  "total_tools": 42,
  "storage_path": "/app/data/tool_embeddings.json",
  "model": "all-MiniLM-L6-v2"
}
```

### 6. Delete Specific Tools
```bash
DELETE /api/tools/delete
Content-Type: application/json
```
**Request**:
```json
{
  "tool_names": ["getUserProfile", "createOrder"]
}
```

**Response**:
```json
{
  "deleted_count": 2,
  "not_found": [],
  "total_tools_remaining": 40,
  "message": "Successfully deleted 2 tools. 0 tools not found."
}
```

### 7. Clear All Tools
```bash
DELETE /api/tools/clear
```

---

## MCP Tools

### Using MCP Tools in Claude Desktop

**Configuration** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "one-mcp": {
      "command": "python",
      "args": [
        "/path/to/one-mcp/app.py",
        "--transport", "stdio",
        "--port", "8004"
      ]
    }
  }
}
```

### Available MCP Tools

| Tool Name | Purpose | Parameters |
|-----------|---------|------------|
| `echo_message` | Test tool | `message: str` |
| `add` | Add numbers | `a: int, b: int` |
| `multiply` | Multiply numbers | `a: int, b: int` |
| `search_tool` | Search for tools | `query: str, k: int` |
| `delete_tools_by_names` | Delete tools | `tool_names: List[str]` |
| `upload_tools_json` | Upload tools | `tools: List[Dict]` |
| `get_stats` | Get statistics | None |
| `clear_tools` | Clear all tools | None |

---

## Data Flow

### Complete Request-Response Cycle

```
┌────────────┐
│   Client   │
└─────┬──────┘
      │
      │ HTTP Request or MCP Call
      ▼
┌─────────────────────────────┐
│   FastAPI / MCP Handler     │
│  - Validate request         │
│  - Parse parameters         │
└─────┬───────────────────────┘
      │
      │ Call method
      ▼
┌─────────────────────────────┐
│      Tools Store            │
│  - Access in-memory data    │
│  - Perform operations       │
│  - Generate embeddings      │
└─────┬───────────────────────┘
      │
      │ (if search)
      ▼
┌─────────────────────────────┐
│  Sentence Transformer       │
│  - Encode query             │
│  - Compute similarities     │
└─────┬───────────────────────┘
      │
      │ Results
      ▼
┌─────────────────────────────┐
│   Response Formatting       │
│  - Serialize to JSON        │
│  - Include metadata         │
└─────┬───────────────────────┘
      │
      │ HTTP Response or MCP Result
      ▼
┌────────────┐
│   Client   │
└────────────┘
```

---

## Deployment

### Local Development

```bash
# Clone repository
git clone https://github.com/freakynit/one-mcp.git
cd one-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py --transport stdio,http --port 8003
```

### Docker Deployment

**Build Image**:
```bash
docker build -t one-mcp:latest .
```

**Run Container**:
```bash
docker run -d \
  -p 9007:9007 \
  -v $(pwd)/data:/app/data \
  --name one-mcp-server \
  one-mcp:latest
```

**Docker Features**:
- Python 3.11 slim base image
- CPU-only PyTorch (smaller image size)
- Persistent volume for tool storage
- Exposed port 9007
- Environment variable for storage path

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `--transport` | stdio | Transport mode: stdio, http, or both |
| `--port` | 8000 | HTTP server port |
| `--host` | 0.0.0.0 | Host to bind to |
| `--storage_path` | tool_embeddings.json | Path to storage file |

---

## Use Cases

### 1. API Discovery for Development Teams

**Scenario**: Large organization with 500+ API endpoints across multiple services

**Solution**:
```bash
# Upload all API definitions
curl -X POST http://localhost:8003/api/tools/upload-file \
  -F "file=@all_apis.json"

# Developers search using natural language
curl -X POST http://localhost:8003/api/tools/search \
  -d '{"query": "send email notification", "k": 5}'
```

**Benefits**:
- Developers find relevant APIs without reading documentation
- Reduces time spent searching for the right endpoint
- Improves API discoverability

### 2. AI Assistant Integration

**Scenario**: Integrate with Claude Desktop for intelligent tool selection

**Configuration**:
```json
{
  "mcpServers": {
    "company-apis": {
      "command": "python",
      "args": ["/path/to/app.py", "--transport", "stdio"]
    }
  }
}
```

**User Interaction**:
```
User: "I need to update a user's email address"
Claude: [Calls search_tool with query "update user email"]
Claude: "I found the updateUserProfile tool which can help..."
```

### 3. API Gateway Tool Registry

**Scenario**: Maintain a central registry of available microservice endpoints

**Implementation**:
- Each microservice registers its APIs on startup
- API gateway uses semantic search to route requests
- Automatic documentation generation

### 4. Developer Onboarding

**Scenario**: New developers need to learn available APIs

**Approach**:
- Provide one-mcp server URL
- Developers explore APIs using natural language queries
- Faster ramp-up time compared to reading documentation

---

## Technical Deep Dive

### Embedding Generation Details

**Model Architecture**:
- 6-layer transformer with 384-dimensional output
- Trained on 1B+ sentence pairs
- Optimized for semantic similarity tasks

**Serialization Strategy**:
```python
def _serialize_tool(self, tool: Dict[str, Any]) -> str:
    parts = []

    # Name and description get highest weight
    if "name" in tool:
        parts.append(f"Name: {tool['name']}")
    if "description" in tool:
        parts.append(f"Description: {tool['description']}")

    # Other fields included but lower impact
    remaining = {k: v for k, v in tool.items()
                if k not in ["name", "description"]}
    if remaining:
        parts.append(json.dumps(remaining))

    return " | ".join(parts)
```

### Similarity Computation

**Cosine Similarity Formula**:
```
similarity = (A · B) / (||A|| × ||B||)
```

Where:
- A = query embedding
- B = tool embedding
- · = dot product
- ||·|| = Euclidean norm

**Implementation**:
```python
from sklearn.metrics.pairwise import cosine_similarity

similarities = cosine_similarity(query_embedding, tool_embeddings)[0]
top_k_indices = np.argsort(similarities)[::-1][:k]
```

### Performance Considerations

**Memory Usage**:
- Model: ~90MB in RAM
- Embeddings: ~1.5KB per tool (384 floats × 4 bytes)
- 1000 tools ≈ 1.5MB embeddings

**Latency**:
- Query encoding: ~5-10ms on CPU
- Similarity computation: ~0.1ms for 1000 tools
- Total search time: ~10-20ms

**Scalability**:
- Current: Linear search O(n)
- Optimization options: FAISS, Annoy for approximate nearest neighbors
- Recommended: < 10,000 tools for current implementation

---

## Future Enhancements

### Potential Improvements

1. **Vector Database Integration**: Use FAISS or Qdrant for large-scale deployments
2. **Multi-tenancy**: Separate tool stores per organization
3. **Authentication**: Add API key or OAuth support
4. **Tool Versioning**: Track changes to tool definitions
5. **Analytics**: Usage tracking and popular tool insights
6. **Batch Operations**: Bulk upload/delete endpoints
7. **Tool Categories**: Organize tools by domain/service
8. **Advanced Filters**: Filter by method, service, parameters

---

## Troubleshooting

### Common Issues

**Issue**: Embeddings not loading on startup
```
Error loading tools from disk: ...
```
**Solution**: Check file permissions and JSON syntax in `tool_embeddings.json`

**Issue**: Poor search results
```
All similarity scores < 0.3
```
**Solution**:
- Ensure tool descriptions are detailed and descriptive
- Check if query matches domain vocabulary
- Consider adding more context to queries

**Issue**: Port already in use
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change port with `--port` or kill existing process

---

## Contributing

The project welcomes contributions in areas like:
- Additional MCP tools
- Performance optimizations
- Documentation improvements
- Test coverage
- Bug fixes

---

## License

MIT License - See LICENSE file for details

---

## Summary

**one-mcp** is a production-ready MCP server that combines modern web APIs with machine learning-powered semantic search. Its dual-transport architecture makes it flexible for various deployment scenarios, from local AI assistants to cloud-based API gateways. The project demonstrates effective integration of FastAPI, MCP, and ML embeddings to solve the practical problem of API discovery and tool management.

**Key Strengths**:
- Simple, clean architecture
- Practical use of ML for improved UX
- Flexible deployment options
- Well-documented API
- Active development (WIP status indicates ongoing improvements)
