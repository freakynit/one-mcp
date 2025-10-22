# 🧠 one-mcp

> WIP


## 🚀 Overview

**one-mcp** is a lightweight **MCP (Model Context Protocol)** server built using **FastAPI** that enables intelligent tool management and semantic search for APIs.
It allows you to upload, manage, and query API tools using natural language — powered by modern embedding models via `sentence-transformers`.

---

## ✨ Features

* 🔍 **Semantic Search:** Find relevant API tools based on descriptive queries.
* 📤 **Upload Tools:** Add new API tools via JSON body or file upload.
* 🗑️ **Delete Tools:** Remove specific tools by name (supports batch deletion).
* 🧾 **Tool Statistics:** Get insights on stored tools.
* 🧹 **Tool Management:** Clear, inspect, or modify your tool store easily.
* ⚡ **FastAPI Backend:** High-performance, async-ready backend server.
* 🤝 **MCP Compatibility:** Easily integrates with MCP-enabled clients and workflows.

---

## 🧩 Project Structure

```
one-mcp/
├── app.py              # Main FastAPI application entry point
├── api.py              # API routes and endpoints
├── mcp_tools.py        # MCP tool handlers and utility functions
├── models.py           # Pydantic and data models
├── tools_store.py      # In-memory or persistent store for tools
├── test_specs.json     # Sample tool dataset
├── CURLS.md            # Example cURL commands for testing API endpoints
├── requirements.txt    # Project dependencies
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
fastapi
uvicorn
fastmcp
sentence-transformers
scikit-learn
numpy
python-multipart
```

---

## 🧠 Running the Server

Start the FastAPI MCP server:

```bash
python app.py --transport stdio,http --port 8003
```

By default, the server starts at:
👉 `http://localhost:8003`

---

## 🧪 Testing the API

You can test all available endpoints using cURL.
See full examples in [CURLS.md](./CURLS.md).

### Example Commands

#### Check Server Status

```bash
curl http://localhost:8003/api/status
```

#### Upload Tools via JSON

```bash
curl -X POST http://localhost:8003/api/tools/upload-json \
  -H "Content-Type: application/json" \
  -d '{"tools": [{"name": "getUserProfile", "description": "Retrieves user profile"}]}'
```

#### Search for Similar Tools

```bash
curl -X POST http://localhost:8003/api/tools/search \
  -H "Content-Type: application/json" \
  -d '{"query": "how to get user info", "k": 3}'
```

#### Delete Specific Tools

```bash
curl -X DELETE http://localhost:8003/api/tools/delete \
  -H "Content-Type: application/json" \
  -d '{"tool_names": ["getUserProfile", "updateUserSettings"]}'
```

All endpoints return structured JSON with similarity scores for search queries.

---

## 🧰 Example MCP Configuration

To integrate with an MCP client:

```json
{
  "mcpServers": {
    "test-mcp-server": {
      "command": "python",
      "args": [
        "/Users/nitinbansal/dev/gitlab/python/one-mcp/app.py",
        "--transport", "stdio,http",
        "--port", "8004"
      ]
    }
  }
}
```

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

