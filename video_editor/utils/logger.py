import logging
import sys
from datetime import datetime

class MediaLogger:
    def __init__(self):
        self.logger = logging.getLogger("media_manipulator")
        self.logger.setLevel(logging.DEBUG)
        
        # Create console handler with formatting
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(handler)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def success(self, message: str):
        # Using info level with SUCCESS prefix
        self.logger.info(f"SUCCESS: {message}")

# Global logger instance
logger = MediaLogger()