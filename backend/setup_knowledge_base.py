#!/usr/bin/env python3
"""
Setup script to initialize the RAG knowledge base.
Run this script to populate the vector database with knowledge from knowledge.txt
"""
import os
import sys
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from rag import initialize_knowledge_base, get_rag_system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Initialize the knowledge base from knowledge.txt file."""
    
    # Path to knowledge file
    knowledge_file = "./resources/knowledge.md"
    
    if not os.path.exists(knowledge_file):
        logger.error(f"Knowledge file not found: {knowledge_file}")
        logger.info("Please create a knowledge.md file in the resources/ directory with information about Manas.")
        return False
    
    logger.info("Starting knowledge base initialization...")
    logger.info(f"Knowledge file: {knowledge_file}")
    
    try:
        # Initialize the knowledge base
        success = initialize_knowledge_base(knowledge_file)
        
        if success:
            logger.info("✅ Knowledge base initialized successfully!")
            
            # Get collection info
            rag = get_rag_system()
            info = rag.get_collection_info()
            logger.info(f"Collection info: {info}")
            
            # Test retrieval
            logger.info("\n🧪 Testing retrieval with sample queries...")
            test_queries = [
                "What programming languages does Manas know?",
                "What is Manas's experience with web development?",
                "Tell me about Manas's projects"
            ]
            
            for query in test_queries:
                logger.info(f"\nQuery: {query}")
                context = rag.retrieve_context(query, top_k=3)
                if context:
                    logger.info("Retrieved context:")
                    for i, sentence in enumerate(context, 1):
                        logger.info(f"  {i}. {sentence}")
                else:
                    logger.warning("No context retrieved")
            
            logger.info("\n✅ Setup completed successfully!")
            logger.info("The chatbot is now ready to use with RAG-enhanced responses.")
            return True
            
        else:
            logger.error("❌ Failed to initialize knowledge base")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during setup: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

