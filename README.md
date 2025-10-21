# 🧠 one-mcp


## 🚀 Overview

**one-mcp** is a lightweight **MCP (Model Context Protocol)** server built using **FastAPI** that enables intelligent specification management and semantic search for APIs.
It allows you to upload, manage, and query API specifications using natural language — powered by modern embedding models via `sentence-transformers`.

---

## ✨ Features

* 🔍 **Semantic Search:** Find relevant API specs based on descriptive queries.
* 📤 **Upload Specs:** Add new API specs via JSON body or file upload.
* 🧾 **Spec Statistics:** Get insights on stored specifications.
* 🧹 **Spec Management:** Clear, inspect, or modify your spec store easily.
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
├── spec_store.py       # In-memory or persistent store for specifications
├── test_specs.json     # Sample specification dataset
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
python app.py --both --port 8003
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

#### Upload Specs via JSON

```bash
curl -X POST http://localhost:8003/api/specs/upload-json \
  -H "Content-Type: application/json" \
  -d '{"specs": [{"name": "getUserProfile", "description": "Retrieves user profile"}]}'
```

#### Search for Similar Specs

```bash
curl -X POST http://localhost:8003/api/specs/search \
  -H "Content-Type: application/json" \
  -d '{"query": "how to get user info", "k": 3}'
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
        "/path/to/one-mcp/app.py",
        "--both",
        "--port", "8000"
      ]
    }
  }
}
```

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

