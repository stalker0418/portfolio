"""
RAG (Retrieval Augmented Generation) module for portfolio chatbot.
Handles embedding generation, vector storage, and context retrieval.
"""
import os
import logging
from typing import List, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

logger = logging.getLogger(__name__)


class RAGSystem:
    """
    Simple and efficient RAG system using ChromaDB and SentenceTransformers.
    Optimized for low latency and simplicity.
    """
    
    def __init__(self, 
                 db_path: str = "./vector_db",
                 collection_name: str = "portfolio_knowledge",
                 model_name: str = "all-MiniLM-L6-v2"):  # Fast, lightweight model
        """
        Initialize RAG system with ChromaDB and SentenceTransformers.
        
        Args:
            db_path: Path to ChromaDB storage
            collection_name: Name of the collection in ChromaDB
            model_name: SentenceTransformers model name (optimized for speed)
        """
        self.db_path = db_path
        self.collection_name = collection_name
        self.model_name = model_name
        
        # Initialize embedding model (lightweight for speed)
        logger.info(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Portfolio knowledge base"}
            )
            logger.info(f"Created new collection: {collection_name}")
    
    def load_knowledge_from_file(self, file_path: str) -> None:
        """
        Load knowledge from a text file and store in vector database.
        Each sentence becomes a separate document for fine-grained retrieval.
        
        Args:
            file_path: Path to the knowledge text file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Knowledge file not found: {file_path}")
        
        logger.info(f"Loading knowledge from: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into meaningful chunks (optimized for Markdown)
        # First try to split by double newlines (paragraphs), then by sentences
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        sentences = []
        for paragraph in paragraphs:
            # If paragraph is short enough, keep as one chunk
            if len(paragraph) <= 200:
                sentences.append(paragraph)
            else:
                # Split longer paragraphs into sentences
                para_sentences = [s.strip() for s in paragraph.split('.') if s.strip()]
                sentences.extend(para_sentences)
        
        # Filter out very short chunks (likely headers or incomplete sentences)
        sentences = [s for s in sentences if len(s) > 20]
        
        if not sentences:
            logger.warning("No sentences found in knowledge file")
            return
        
        # Clear existing data
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Portfolio knowledge base"}
            )
            logger.info("Cleared existing knowledge base")
        except Exception as e:
            logger.warning(f"Could not clear existing collection: {e}")
        
        # Generate embeddings for all sentences
        logger.info(f"Generating embeddings for {len(sentences)} sentences...")
        embeddings = self.embedding_model.encode(sentences, show_progress_bar=True)
        
        # Prepare data for ChromaDB
        ids = [f"sentence_{i}" for i in range(len(sentences))]
        documents = sentences
        metadatas = [{"source": "knowledge.txt", "sentence_id": i} for i in range(len(sentences))]
        
        # Store in ChromaDB
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Successfully stored {len(sentences)} sentences in vector database")
    
    def retrieve_context(self, query: str, top_k: int = 10) -> List[str]:
        """
        Retrieve relevant context for a given query.
        
        Args:
            query: User query to find relevant context for
            top_k: Number of top relevant sentences to retrieve
            
        Returns:
            List of relevant sentences
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.encode([query])
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=top_k
            )
            
            # Extract documents (sentences)
            if results['documents'] and len(results['documents']) > 0:
                relevant_sentences = results['documents'][0]  # First (and only) query result
                logger.info(f"Retrieved {len(relevant_sentences)} relevant sentences")
                return relevant_sentences
            else:
                logger.warning("No relevant context found")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def get_collection_info(self) -> dict:
        """Get information about the current collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "model_name": self.model_name
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"error": str(e)}


# Global RAG instance (initialized when module is imported)
_rag_instance: Optional[RAGSystem] = None


def get_rag_system() -> RAGSystem:
    """
    Get or create the global RAG system instance.
    Singleton pattern for efficiency.
    """
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGSystem()
    return _rag_instance


def initialize_knowledge_base(knowledge_file_path: str = "./resources/knowledge.txt") -> bool:
    """
    Initialize the knowledge base from a text file.
    
    Args:
        knowledge_file_path: Path to the knowledge text file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        rag = get_rag_system()
        rag.load_knowledge_from_file(knowledge_file_path)
        return True
    except Exception as e:
        logger.error(f"Failed to initialize knowledge base: {e}")
        return False


def retrieve_relevant_context(query: str, top_k: int = 10) -> List[str]:
    """
    Retrieve relevant context for a query (convenience function).
    
    Args:
        query: User query
        top_k: Number of relevant sentences to retrieve
        
    Returns:
        List of relevant sentences
    """
    rag = get_rag_system()
    return rag.retrieve_context(query, top_k)

