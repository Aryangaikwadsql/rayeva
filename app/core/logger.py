"""Logging config."""
import logging
from typing import Dict, Any

from loguru import logger as loguru_logger

# Configure loguru to behave like standard logging for compatibility
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level
        level = logger.level(getattr(record, 'levelname', 'INFO')).name
        loguru_logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

# Setup
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

loguru_logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="1 day", level="INFO", format="{time} {level} {message}")

logger = loguru_logger

