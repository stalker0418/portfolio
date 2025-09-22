#!/usr/bin/env python3
"""
Startup script for portfolio backend with RAG database initialization.

This script:
1. Updates the RAG database with latest resources
2. Starts the FastAPI application

This should be used as the main entry point for deployment.
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def update_rag_database():
    """Update RAG database before starting the server."""
    logger = logging.getLogger(__name__)
    logger.info("🔄 Updating RAG database before server startup...")
    
    try:
        # Import and run RAG update
        from rag_system import RAGSystem
        
        logger.info("Initializing RAG system...")
        rag_system = RAGSystem()
        
        logger.info("Processing all resources...")
        success = rag_system.process_all_resources()
        
        if success:
            logger.info("✅ RAG database updated successfully")
            stats = rag_system.get_database_stats()
            logger.info(f"📊 Database Statistics:")
            logger.info(f"   - Total documents: {stats.get('total_documents', 0)}")
            
            if 'source_types' in stats:
                for source_type, count in stats['source_types'].items():
                    logger.info(f"   - {source_type}: {count} documents")
            
            return True
        else:
            logger.error("❌ Failed to update RAG database")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error updating RAG database: {str(e)}")
        # Log the full traceback for debugging
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

def start_server():
    """Start the FastAPI server."""
    logger = logging.getLogger(__name__)
    logger.info("Starting FastAPI server...")
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    try:
        import uvicorn
        from app import app
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"❌ Error starting server: {str(e)}")
        sys.exit(1)

def main():
    """Main startup function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Starting Portfolio Backend with RAG System")
    
    # Check if RAG update should be skipped (useful for development)
    skip_rag_update = os.getenv("SKIP_RAG_UPDATE", "false").lower() == "true"
    
    if skip_rag_update:
        logger.info("⏭️  Skipping RAG database update (SKIP_RAG_UPDATE=true)")
    else:
        # Update RAG database first
        logger.info("📚 Updating RAG database as part of deployment...")
        if not update_rag_database():
            # In production, we want to continue even if RAG update fails
            # The chatbot will still work, just without enhanced context
            logger.warning("⚠️  RAG database update failed, but continuing with server startup...")
            logger.warning("💡 The chatbot will work with basic functionality")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
