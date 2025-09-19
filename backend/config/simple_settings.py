"""Simple application configuration settings."""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Simple application settings."""
    
    # API Configuration
    api_title: str = "Manas Sanjay Portfolio API"
    api_description: str = "AI-powered portfolio backend with RAG chatbot"
    api_version: str = "1.0.0"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://manas-sanjay-pakalapati-portfolio.vercel.app",
        "https://*.vercel.app"
    ]
    
    # AI Model Configuration
    default_model: str = "together"
    together_api_key: Optional[str] = os.getenv("TOGETHER_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Model-specific settings
    model_temperature: float = 0.7
    model_max_tokens: int = 1000
    
    # Resource paths
    resources_dir: Path = Path("resources")
    resources_config_file: str = "resources.yaml"
    
    # Vector Database Configuration
    vector_db_path: str = "./vector_db"
    chunk_size: int = 1000
    chunk_overlap: int = 200


# Global settings instance
settings = Settings()
