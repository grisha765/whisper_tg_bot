import logging
import os

from config.config import Config 
RESET = "\x1b[0m"
WHITE = "\x1b[0m"
COLORS = {
    'DEBUG': "\x1b[34m",      # Blue
    'INFO': "\x1b[32m",       # Green
    'WARNING': "\x1b[33m",    # Yellow
    'ERROR': "\x1b[31m",      # Red
    'CRITICAL': "\x1b[41m",   # Red background
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, RESET)
        message = super().format(record)
        filename = os.path.splitext(os.path.basename(record.pathname))[0]
        return f"{log_color}{record.levelname}{RESET}{WHITE}: {filename}: {message}{RESET}"

def setup_logging(name='my_app'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = ColoredFormatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, Config.log_level, logging.INFO))
    return logger

