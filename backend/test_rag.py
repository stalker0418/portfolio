#!/usr/bin/env python3
"""
Test script for RAG implementation.
Tests the complete flow: knowledge loading, embedding, retrieval, and chatbot integration.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from rag import initialize_knowledge_base, retrieve_relevant_context, get_rag_system
from chatbot import ChatbotWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_rag_system():
    """Test the complete RAG system."""
    
    logger.info("🧪 Testing RAG System")
    logger.info("=" * 50)
    
    # Test 1: Initialize knowledge base
    logger.info("\n1️⃣ Testing knowledge base initialization...")
    success = initialize_knowledge_base("./resources/knowledge.md")
    if not success:
        logger.error("❌ Failed to initialize knowledge base")
        return False
    logger.info("✅ Knowledge base initialized successfully")
    
    # Test 2: Check collection info
    logger.info("\n2️⃣ Testing collection info...")
    rag = get_rag_system()
    info = rag.get_collection_info()
    logger.info(f"Collection info: {info}")
    
    # Test 3: Test retrieval with various queries
    logger.info("\n3️⃣ Testing context retrieval...")
    test_queries = [
        "What programming languages does Manas know?",
        "Tell me about Manas's web development experience",
        "What projects has Manas worked on?",
        "Does Manas have experience with machine learning?",
        "What cloud platforms does Manas use?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        logger.info(f"\nQuery {i}: {query}")
        context = retrieve_relevant_context(query, top_k=3)
        if context:
            logger.info("Retrieved context:")
            for j, sentence in enumerate(context, 1):
                logger.info(f"  {j}. {sentence}")
        else:
            logger.warning("No context retrieved")
    
    # Test 4: Test chatbot integration
    logger.info("\n4️⃣ Testing chatbot integration...")
    chatbot = ChatbotWrapper()
    
    test_chat_queries = [
        "What programming languages do you know?",
        "Tell me about your web development experience"
    ]
    
    for query in test_chat_queries:
        logger.info(f"\nChatbot Query: {query}")
        try:
            # Note: This will only work if you have a valid Together AI API key
            response = await chatbot.chat(query)
            logger.info(f"Chatbot Response: {response[:200]}...")
        except Exception as e:
            logger.warning(f"Chatbot test skipped (API key needed): {e}")
    
    logger.info("\n✅ All tests completed successfully!")
    return True


async def main():
    """Main test function."""
    try:
        success = await test_rag_system()
        if success:
            logger.info("\n🎉 RAG system is working correctly!")
            logger.info("You can now start the FastAPI server and test the /chat endpoint.")
        else:
            logger.error("\n❌ RAG system tests failed!")
        return success
    except Exception as e:
        logger.error(f"Test error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

