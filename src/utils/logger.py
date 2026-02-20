"""
Logging configuration for the Dynamic Job Matching Platform
"""
import logging
import sys
from typing import Optional


def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up and configure a logger for the application.
    
    Args:
        name: Name of the logger (defaults to root logger)
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or __name__)
    
    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Console handler with detailed formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Detailed format with timestamp, level, and message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger
