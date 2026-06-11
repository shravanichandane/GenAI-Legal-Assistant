"""
Structured logging setup for the LegalSight AI platform.

Usage
-----
    from app.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("Server started")
    logger.error("Something went wrong", exc_info=True)

Why structured logging?
-----------------------
* In production, ``print()`` statements vanish into the void.
* A proper logger lets us:
  - Filter by severity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Write to files for post-mortem debugging
  - Include timestamps and module names automatically
  - Disable/enable debug output via a single env var (LOG_LEVEL)

Interview Tip
-------------
Q: "Why not just use print()?"
A: print() writes to stdout with no metadata. logging gives us severity
   levels, timestamps, module context, and the ability to route output to
   files, monitoring services (e.g. Datadog, CloudWatch), or suppress
   noisy debug output in production — all without changing a single line
   of application code.
"""

import logging
import sys
from pathlib import Path

from app.config import settings


def setup_logging() -> None:
    """Configure the root logger for the entire application.

    Call this once at startup (e.g. in ``main.py``).
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Ensure the logs directory exists
    settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = settings.LOGS_DIR / "legalsight.log"

    # Format: 2026-06-01 16:12:00 | INFO | app.services.llm | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (always present)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # File handler (rotates manually; for production use RotatingFileHandler)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers on repeated calls
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a child logger. Use ``__name__`` as *name* by convention.

    Example::

        logger = get_logger(__name__)
        logger.info("Processing document %s", doc_id)
    """
    return logging.getLogger(name)
