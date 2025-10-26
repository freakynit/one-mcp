import sys

from logging_setup import setup_logging, get_logger
from config import ServerConfig, create_argument_parser
from mcp_server import MCPServer
from api import create_app
from mcp_tools import mcp


# Configure logging at application startup
setup_logging(
    log_level="DEBUG",
    log_file="logs/app.log",
    max_bytes=10_000_000,  # 10 MB
    backup_count=3
)

logger = get_logger(__name__)


# Initializations for uvicorn
config = None
app = None


def initialize_app():
    """Initialize the app for uvicorn when imported."""
    global config, app
    if app is None:
        config = ServerConfig.default()
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
