from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Set

@dataclass
class ServerConfig:
    """Configuration for the MCP server."""
    transports: Set[str]
    port: int
    host: str
    storage_path: str
    
    @classmethod
    def from_args(cls, args) -> ServerConfig:
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
    
    @classmethod
    def default(cls) -> ServerConfig:
        """Create default configuration."""
        return cls(
            transports={"stdio"},
            port=8000,
            host="0.0.0.0",
            storage_path="tool_embeddings.json"
        )


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
