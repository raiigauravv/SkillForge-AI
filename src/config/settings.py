"""
Configuration settings for SkillForge AI
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Settings
    APP_NAME: str = "SkillForge AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "localhost"
    PORT: int = 8000
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # AI Model Configuration
    MODEL_VERSION: str = "gpt-4o-mini"
    MAX_TOKENS: int = 1200
    TEMPERATURE: float = 0.3
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./workflows.db"
    VECTOR_DB_PATH: str = "./data/vectordb"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # CrewAI Configuration
    CREW_MAX_AGENTS: int = 10
    TASK_TIMEOUT: int = 300
    WORKFLOW_MAX_STEPS: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
