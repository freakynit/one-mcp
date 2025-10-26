# logging_setup.py
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from threading import Lock
from typing import Optional

_DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"

_configured = False
_config_lock = Lock()


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = "logs/app.log",
    max_bytes: int = 5_000_000,
    backup_count: int = 5,
    enable_console: bool = True,
):
    """
    Configure root logging once with console + rotating file handlers.
    Thread-safe and safe to call multiple times.
    """
    global _configured
    
    if _configured:
        return
    
    with _config_lock:
        if _configured:  # Double-check after acquiring lock
            return

        level_name = (log_level or os.getenv("LOG_LEVEL") or "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)

        root = logging.getLogger()
        root.setLevel(level)
        root.handlers.clear()

        formatter = logging.Formatter(_DEFAULT_FORMAT, datefmt=_DATEFMT)

        # Console handler
        if enable_console:
            console = logging.StreamHandler(stream=sys.stdout)
            console.setFormatter(formatter)
            root.addHandler(console)

        # Rotating file handler
        if log_file and log_file.strip():
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            root.addHandler(file_handler)

        # Quiet noisy libraries
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

        _configured = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger. If logging hasn't been configured yet, configure with defaults.
    """
    if not _configured:
        setup_logging()
    return logging.getLogger(name if name else __name__)

