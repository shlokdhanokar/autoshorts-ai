"""
Logging configuration for AutoShorts AI system.
"""

from loguru import logger
import sys
from config.settings import settings


def setup_logging():
    """Configure logging for the application."""
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with formatting
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # Add file handler for persistent logs
    logger.add(
        "logs/autoshorts_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # Rotate at midnight
        retention="30 days",  # Keep logs for 30 days
        level="DEBUG",  # Log everything to file
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    # Add error-specific log file
    logger.add(
        "logs/errors_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="90 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    logger.info(f"Logging initialized - Level: {settings.log_level}, Environment: {settings.environment}")
    
    return logger


# Initialize logging
log = setup_logging()
