import argparse
import asyncio
import logging
import signal
import sys
import threading
import time
from dataclasses import dataclass
from typing import Set

import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import with error handling
try:
    from api import create_app
    from mcp_tools import mcp
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)


@dataclass
class ServerConfig:
    """Configuration for the MCP server."""
    transports: Set[str]
    port: int
    host: str
    storage_path: str
    
    @classmethod
    def from_args(cls, args) -> 'ServerConfig':
        """Create configuration from command line arguments."""
        # Normalize and validate transports
        raw_transports = [t.strip().lower() for t in args.transport.split(",")]
        valid_transports = {"stdio", "http"}
        invalid = [t for t in raw_transports if t not in valid_transports]
        if invalid:
            raise ValueError(f"Invalid transport(s): {', '.join(invalid)}. Choose from {', '.join(valid_transports)}.")
        
        return cls(
            transports=set(raw_transports),
            port=args.port,
            host=args.host,
            storage_path=args.storage_path
        )


class MCPServer:
    """MCP Server with support for multiple transports."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.http_thread = None
        self.http_server = None
        self.shutdown_requested = False
        
        # Create the combined app
        try:
            self.app = create_app(mcp, config.storage_path)
            logger.info(f"Created app with storage path: {config.storage_path}")
        except Exception as e:
            logger.error(f"Failed to create app: {e}")
            raise
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}, initiating graceful shutdown...")
            self.shutdown_requested = True
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run_http_server(self):
        """Run the HTTP server using uvicorn with proper shutdown handling."""
        try:
            logger.info(f"Starting HTTP server on {self.config.host}:{self.config.port}")
            
            # Create uvicorn server configuration
            config = uvicorn.Config(
                self.app,
                host=self.config.host,
                port=self.config.port,
                log_level="info"
            )
            
            # Create server instance
            self.http_server = uvicorn.Server(config)
            
            # Run the server
            asyncio.run(self.http_server.serve())
            
        except Exception as e:
            logger.error(f"HTTP server failed: {e}")
            if not self.shutdown_requested:
                raise
    
    def start_http_server_thread(self):
        """Start HTTP server in a background thread."""
        self.http_thread = threading.Thread(target=self.run_http_server, daemon=True)
        self.http_thread.start()
        
        # Give the server a moment to start
        time.sleep(1)
        logger.info(f"HTTP server thread started on {self.config.host}:{self.config.port}")
    
    def run_stdio_server(self):
        """Run the stdio MCP server."""
        try:
            logger.info("Starting MCP stdio server...")
            mcp.run()
        except Exception as e:
            logger.error(f"MCP stdio server failed: {e}")
            if not self.shutdown_requested:
                raise
    
    def run(self):
        """Run the server with the configured transports."""
        logger.info(f"Using transports: {', '.join(sorted(self.config.transports))}")
        logger.info(f"Configuration: port={self.config.port}, host={self.config.host}, storage_path={self.config.storage_path}")
        
        self.setup_signal_handlers()
        
        try:
            if {"stdio", "http"}.issubset(self.config.transports):
                # Dual transport mode
                logger.info("Running in dual transport mode (stdio + http)")
                self.start_http_server_thread()
                self.run_stdio_server()
                
            elif "http" in self.config.transports:
                # HTTP only mode
                logger.info("Running in HTTP-only mode")
                self.run_http_server()
                
            elif "stdio" in self.config.transports:
                # Stdio only mode
                logger.info("Running in stdio-only mode")
                self.run_stdio_server()
                
            else:
                logger.warning("No valid transports configured")
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Perform cleanup on shutdown."""
        logger.info("Shutting down server...")
        self.shutdown_requested = True
        
        # Shutdown HTTP server if running
        if self.http_server:
            logger.info("Shutting down HTTP server...")
            self.http_server.should_exit = True
            # Give it a moment to shutdown gracefully
            time.sleep(0.5)
        
        if self.http_thread and self.http_thread.is_alive():
            logger.info("Waiting for HTTP server thread to finish...")
            self.http_thread.join(timeout=5.0)
            if self.http_thread.is_alive():
                logger.warning("HTTP server thread did not terminate gracefully")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="Run FastMCP server with transport option.")
    parser.add_argument(
        "--transport", 
        default="stdio", 
        help="Comma-separated transports to enable (choices: stdio, http; default: stdio)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port number for the server (default: 8000)"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--storage_path", 
        default="tool_embeddings.json", 
        help="Path to store tool embeddings (default: tool_embeddings.json)"
    )
    return parser


# Create the app instance for uvicorn
config = None
app = None

def initialize_app():
    """Initialize the app for uvicorn when imported."""
    global config, app
    if app is None:
        # Use default config when imported as module
        default_args = argparse.Namespace(
            transport="stdio",
            port=8000,
            host="0.0.0.0",
            storage_path="tool_embeddings.json"
        )
        config = ServerConfig.from_args(default_args)
        try:
            app = create_app(mcp, config.storage_path)
        except Exception as e:
            logger.error(f"Failed to initialize app: {e}")
            raise

# Initialize app for uvicorn
initialize_app()


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        config = ServerConfig.from_args(args)
        server = MCPServer(config)
        server.run()
    except ValueError as e:
        parser.error(str(e))
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
