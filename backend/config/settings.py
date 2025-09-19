"""Application configuration settings."""

import os
from typing import Optional, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    api_title: str = Field(default="Manas Sanjay Portfolio API", env="API_TITLE")
    api_description: str = Field(default="AI-powered portfolio backend with RAG chatbot", env="API_DESCRIPTION")
    api_version: str = Field(default="1.0.0", env="API_VERSION")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # CORS Configuration
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://manas-sanjay-pakalapati-portfolio.vercel.app",
            "https://*.vercel.app"
        ]
    )
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # AI Model Configuration
    default_model: str = Field(default="together", env="DEFAULT_MODEL")
    together_api_key: Optional[str] = Field(default=None, env="TOGETHER_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # Model-specific settings
    model_temperature: float = Field(default=0.7, env="MODEL_TEMPERATURE")
    model_max_tokens: int = Field(default=1000, env="MODEL_MAX_TOKENS")
    
    # Resource paths
    resources_dir: Path = Field(default=Path("resources"), env="RESOURCES_DIR")
    resources_config_file: str = Field(default="resources.yaml", env="RESOURCES_CONFIG_FILE")
    
    # Vector Database Configuration
    vector_db_path: str = Field(default="./vector_db", env="VECTOR_DB_PATH")
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, env="CHUNK_OVERLAP")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        env_ignore_empty = True


# Global settings instance
settings = Settings()
