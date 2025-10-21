from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("API Tools")


@mcp.tool
def echo_message(message: str) -> str:
    """Echo back the given message"""
    return message


@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b


@mcp.tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integer numbers together."""
    return a * b
