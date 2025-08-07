"""
Logging utility for SkillForge AI
"""

import logging
import os
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: str = "./logs/app.log"):
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(log_file).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("crewai").setLevel(logging.INFO)
    
    return logging.getLogger(__name__)
