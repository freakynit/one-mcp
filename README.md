# 🧠 one-mcp

> WIP


## 🚀 Overview

**one-mcp** is a lightweight **MCP (Model Context Protocol)** server built using **FastAPI** that enables intelligent tool management and semantic search for APIs.
It allows you to upload, manage, and query API tools using natural language — powered by modern embedding models via `sentence-transformers`.

The server supports multiple transport modes (stdio, HTTP, or both) and provides both a REST API and MCP tool interface for maximum flexibility.

---

## ✨ Features

* 🔍 **Semantic Search:** Find relevant API tools based on descriptive queries using sentence-transformers embeddings.
* 📤 **Upload Tools:** Add new API tools via JSON body or file upload.
* 🗑️ **Delete Tools:** Remove specific tools by name (supports batch deletion).
* 🧾 **Tool Statistics:** Get insights on stored tools including count, model, and storage path.
* 🧹 **Tool Management:** Clear, inspect, or modify your tool store easily.
* ⚡ **FastAPI Backend:** High-performance, async-ready backend server.
* 🤝 **MCP Compatibility:** Dual interface - REST API and MCP tools for seamless integration.
* 🔄 **Dual Transport:** Support for stdio and HTTP transports simultaneously.
* 💾 **Persistent Storage:** Tools and embeddings saved to disk with automatic loading.
* 📊 **Structured Logging:** Comprehensive logging with rotating file handlers.

---

## 🧩 Project Structure

```
one-mcp/
├── server.py           # Main application entry point with server orchestration
├── mcp_server.py       # MCP server class with multi-transport support
├── api.py              # FastAPI routes and REST endpoints
├── mcp_tools.py        # MCP tool definitions and handlers
├── models.py           # Pydantic models for request/response validation
├── tools_store.py      # Persistent tool storage with embeddings
├── config.py           # Server configuration and argument parsing
├── logging_setup.py    # Centralized logging configuration
├── test_specs.json     # Sample tool dataset for testing
├── CURLS.md            # Example cURL commands for testing API endpoints
├── MCP_TOOLS.md        # MCP tools documentation
├── requirements.txt    # Project dependencies
├── Dockerfile          # Docker containerization (CPU-based dependencies)
└── README.md           # Project documentation (this file)
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/freakynit/one-mcp.git
cd one-mcp
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

```
fastapi>=0.104.0
uvicorn>=0.24.0
fastmcp>=0.2.0
python-multipart>=0.0.6
torch==2.4.1
torchvision==0.19.1
torchaudio==2.4.1
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
numpy>=1.24.0
```

---

## 🧠 Running the Server

> **Note**: The first time you run the server, it will download the `all-MiniLM-L6-v2` model from sentence-transformers. This may take a few seconds depending on your internet connection.

### Start with Dual Transport (stdio + HTTP)

```bash
python server.py --transport stdio,http --port 8003
```

This enables both MCP stdio communication and HTTP REST API access.

### HTTP-only Mode

```bash
python server.py --transport http --port 8003
```

### Stdio-only Mode (for MCP clients)

```bash
python server.py --transport stdio
```

### Using Uvicorn Directly

```bash
uvicorn server:app --host 0.0.0.0 --port 8003
```

### Configuration Options

- `--transport`: Transport mode (stdio, http, or stdio,http) - default: stdio
- `--port`: HTTP port number - default: 8000
- `--host`: Host to bind to - default: 0.0.0.0
- `--storage_path`: Path to store tool embeddings - default: tool_embeddings.json

By default, the server starts at:
👉 `http://localhost:8003` (when HTTP transport is enabled)

The server automatically:
- Creates a `logs/` directory for application logs
- Loads existing tools from `tool_embeddings.json` on startup
- Saves tools to disk after any modification

---

## 🧪 Testing the API

The server provides two interfaces:

1. **REST API**: Available at `/api/*` endpoints (see [CURLS.md](./CURLS.md) for examples)
2. **MCP Tools**: Available via MCP protocol (see [MCP_TOOLS.md](./MCP_TOOLS.md) for documentation)

### REST API Endpoints

All endpoints return structured JSON responses with appropriate status codes.

#### Check Server Status

```bash
curl http://localhost:8003/api/status
```

#### Upload Tools via JSON

```bash
curl -X POST http://localhost:8003/api/tools/upload-json \
  -H "Content-Type: application/json" \
  -d '{"tools": [{"type": "function", "name": "get_weather", "description": "Get the current weather for a specific city.", "parameters": {"type": "object", "properties": {"city": {"type": "string", "description": "The name of the city to get weather for."}}}}]}'
```

#### Upload Tools via File

```bash
curl -X POST http://localhost:8003/api/tools/upload-file \
  -F "file=@test_tools.json;type=application/json"
```

#### Search for Similar Tools

```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{"query": "weather forecast for a city", "k": 3}'
```

#### Get Statistics

```bash
curl http://localhost:8003/api/tools/stats
```

#### Delete Specific Tools

```bash
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{"tool_names": ["get_weather", "get_news_headlines"]}'
```

#### Clear All Tools

```bash
curl -X DELETE http://localhost:8003/api/tools/clear
```

### MCP Access

The MCP endpoint is mounted at `/mcp` for HTTP streaming mode:

```bash
curl http://localhost:8003/mcp
```

For full MCP tool documentation, see [MCP_TOOLS.md](./MCP_TOOLS.md).

For more comprehensive testing examples, see [CURLS.md](./CURLS.md).

---

## 🧰 Example MCP Configuration

To integrate with an MCP client (like Claude Desktop):

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

For dual transport mode (stdio for MCP + HTTP for REST API):

```json
{
  "mcpServers": {
    "one-mcp-server": {
      "command": "python",
      "args": [
        "/absolute/path/to/server.py",
        "--transport", "stdio,http",
        "--port", "8004",
        "--storage_path", "tool_embeddings.json"
      ]
    }
  }
}
```

---

## 🏗️ Architecture

### Components

- **server.py**: Entry point that initializes the app and starts the MCP server
- **mcp_server.py**: Handles multi-transport server orchestration (stdio/HTTP/dual)
- **api.py**: FastAPI application factory and REST endpoint definitions
- **mcp_tools.py**: MCP tool decorators and function implementations
- **tools_store.py**: Singleton store for tool embeddings with search capability
- **models.py**: Pydantic models for type safety and validation
- **config.py**: Configuration management and CLI argument parsing
- **logging_setup.py**: Centralized logging with rotating file handlers

### How It Works

1. **Tool Storage**: Tools are stored with their embeddings using `sentence-transformers`
2. **Semantic Search**: Query embeddings are compared using cosine similarity
3. **Persistence**: Tools automatically saved to `tool_embeddings.json`
4. **Dual Interface**: Same functionality available via REST API and MCP tools
5. **Multi-Transport**: Server can run stdio (for MCP clients) and HTTP simultaneously

---

### Dev
1. Create zip: `zip -r one-mcp.zip . -x "*.git/*" -x ".env" -x ".DS_Store" -x ".dockerignore" -x ".gitignore"`

---

## 🧑‍💻 Contributing

Contributions are welcome!
To contribute:

1. **Fork** the repository
2. **Create** a new feature branch (`git checkout -b feature/my-feature`)
3. **Commit** your changes (`git commit -m "Add my feature"`)
4. **Push** to your fork (`git push origin feature/my-feature`)
5. **Submit a Pull Request**

Before submitting, ensure:

* Code passes linting and basic tests.
* You’ve updated documentation if needed.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

If you encounter any issues or have feature requests:

* Open an issue on [GitHub](https://github.com/freakynit/one-mcp/issues)
* Or contact [@freakynit](https://github.com/freakynit) directly.

