"""Logging configuration for AI Media Monitor."""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(
    name: str,
    log_file: str | None = None,
    level: int = logging.INFO,
    console_output: bool = True,
) -> logging.Logger:
    """
    Setup a logger with both file and console handlers.

    Args:
        name: Logger name (usually __name__)
        log_file: Path to log file. If None, creates one based on timestamp
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Whether to also log to console

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    if log_file is None:
        # Create default log file with timestamp
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"daily_collection_{timestamp}.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler (optional)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        # Simpler format for console
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def setup_daily_collection_logger() -> logging.Logger:
    """Setup logger specifically for daily collection operations."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"daily_collection_{timestamp}.log"

    return setup_logger(
        name="daily_collection", log_file=str(log_file), level=logging.INFO, console_output=True
    )


def log_exception(logger: logging.Logger, message: str, exc_info: bool = True):
    """
    Log an exception with full traceback.

    Args:
        logger: Logger instance
        message: Custom error message
        exc_info: Whether to include exception traceback
    """
    logger.error(message, exc_info=exc_info)


def log_stats(logger: logging.Logger, stats: dict):
    """
    Log statistics in a structured format.

    Args:
        logger: Logger instance
        stats: Dictionary with statistics to log
    """
    logger.info("=== STATISTICS ===")
    for key, value in stats.items():
        logger.info(f"{key}: {value}")
    logger.info("==================")
