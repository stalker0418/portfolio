#!/usr/bin/env python3
"""
Simple runner script for the portfolio backend.
"""
import uvicorn
from app import app

def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
