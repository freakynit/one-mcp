import argparse
import threading
import uvicorn
from api import create_app
from mcp_tools import mcp

parser = argparse.ArgumentParser(description="Run FastMCP server with transport option.")
parser.add_argument("--transport", choices=["stdio", "http"], default="stdio", help="Transport to choose (default: stdio)")
parser.add_argument("--port", type=int, default=8000, help="Port number for the server (default: 8000)")
parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
parser.add_argument("--both", action="store_true", help="Run both uvicorn (HTTP) and MCP stdio together")
args = parser.parse_args()

TRANSPORT = args.transport
PORT = args.port
HOST = args.host

print(f"Using transport: {TRANSPORT}, both={args.both}, port={PORT}, host={HOST}")

# Create the combined app
app = create_app(mcp)


def run_uvicorn():
    uvicorn.run("app:app", host=HOST, port=PORT, reload=False)


if __name__ == "__main__":
    if args.both:
        # Start HTTP server in a background thread
        t = threading.Thread(target=run_uvicorn, daemon=True)
        t.start()
        print(f"HTTP server started on {HOST}:{PORT}")
        print("Starting MCP stdio server...")
        # Block on stdio loop
        mcp.run()
    else:
        if TRANSPORT == "http":
            print(f"Starting HTTP server on {HOST}:{PORT}")
            run_uvicorn()
        else:
            print("Starting MCP stdio server...")
            mcp.run()
