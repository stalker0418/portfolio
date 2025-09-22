#!/usr/bin/env python3
"""
RAG Database Update Script for Portfolio Chatbot

This script processes all resources defined in resources.yaml and updates
the vector database with the latest content. It should be run whenever:
1. New resources are added to resources.yaml
2. Existing resources are updated
3. During deployment to ensure the chatbot has the latest context

Usage:
    python update_rag_database.py [--force] [--verbose]
    
Options:
    --force     Force rebuild of the entire database
    --verbose   Enable verbose logging
    --stats     Show database statistics after update
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from rag_system import RAGSystem

def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    """Main function to update RAG database."""
    parser = argparse.ArgumentParser(
        description="Update RAG database with latest portfolio resources"
    )
    parser.add_argument(
        '--force', 
        action='store_true', 
        help='Force rebuild of the entire database'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--stats', 
        action='store_true', 
        help='Show database statistics after update'
    )
    parser.add_argument(
        '--resources-dir',
        default='resources',
        help='Path to resources directory (default: resources)'
    )
    parser.add_argument(
        '--db-path',
        default='./vector_db',
        help='Path to vector database (default: ./vector_db)'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting RAG database update...")
    logger.info(f"Resources directory: {args.resources_dir}")
    logger.info(f"Database path: {args.db_path}")
    
    try:
        # Initialize RAG system
        rag_system = RAGSystem(
            resources_dir=args.resources_dir,
            db_path=args.db_path
        )
        
        # Clear database if force rebuild is requested
        if args.force:
            logger.info("Force rebuild requested - clearing existing database...")
            try:
                # Delete and recreate collection
                rag_system.chroma_client.delete_collection("portfolio_resources")
                rag_system.collection = rag_system.chroma_client.create_collection(
                    name="portfolio_resources",
                    metadata={"description": "Manas Sanjay Pakalapati's portfolio resources"}
                )
                logger.info("Database cleared successfully")
            except Exception as e:
                logger.warning(f"Could not clear database: {str(e)}")
        
        # Process all resources
        logger.info("Processing resources...")
        success = rag_system.process_all_resources()
        
        if success:
            logger.info("✅ RAG database updated successfully!")
            
            # Show statistics if requested
            if args.stats:
                logger.info("Database Statistics:")
                stats = rag_system.get_database_stats()
                for key, value in stats.items():
                    if key == 'source_types':
                        logger.info(f"  {key}:")
                        for source_type, count in value.items():
                            logger.info(f"    {source_type}: {count} documents")
                    else:
                        logger.info(f"  {key}: {value}")
        else:
            logger.error("❌ Failed to update RAG database")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Error updating RAG database: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
