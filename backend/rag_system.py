"""
RAG (Retrieval-Augmented Generation) System for Portfolio Chatbot.

This module implements a comprehensive RAG system that:
1. Processes various resource types (PDF, web links, etc.)
2. Stores embeddings in a vector database (ChromaDB)
3. Retrieves relevant context for user queries
4. Provides citations and links in responses
"""

import os
import logging
import yaml
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import urlparse, urljoin

# Core dependencies
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests
from bs4 import BeautifulSoup
import PyPDF2
import tiktoken
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# OCR dependencies
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ResourceDocument:
    """Represents a processed document with metadata."""
    id: str
    content: str
    source_type: str  # 'resume', 'linkedin', 'github', 'medium', 'paper', 'project'
    source_url: Optional[str]
    title: str
    description: str
    metadata: Dict[str, Any]
    created_at: datetime
    chunk_index: Optional[int] = None


@dataclass
class RetrievalResult:
    """Represents a retrieved document chunk with relevance score."""
    document: ResourceDocument
    score: float
    rank: int


class ResourceProcessor:
    """Handles processing of different resource types."""
    
    def __init__(self):
        """Initialize the resource processor."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Download NLTK data if needed
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            logger.info("Downloading required NLTK data...")
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    def process_pdf(self, file_path: str, metadata: Dict[str, Any]) -> List[ResourceDocument]:
        """Extract text from PDF file using OCR and create document chunks."""
        try:
            logger.info(f"Processing PDF with OCR: {file_path}")
            text = self._extract_pdf_text_with_ocr(file_path)
            
            if not text.strip():
                logger.warning(f"No text extracted from PDF: {file_path}")
                return []
            
            # Clean and process text
            text = self._clean_text(text)
            chunks = self._chunk_text(text, max_tokens=500)
            
            documents = []
            for i, chunk in enumerate(chunks):
                doc_id = self._generate_doc_id(f"resume_chunk_{i}", chunk)
                documents.append(ResourceDocument(
                    id=doc_id,
                    content=chunk,
                    source_type="resume",
                    source_url=None,
                    title=metadata.get('description', 'Resume'),
                    description=f"Resume content - Chunk {i+1}",
                    metadata={**metadata, 'chunk_index': i, 'total_chunks': len(chunks)},
                    created_at=datetime.now(),
                    chunk_index=i
                ))
            
            logger.info(f"Processed PDF into {len(documents)} chunks using OCR")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            return []
    
    def _extract_pdf_text_with_ocr(self, file_path: str) -> str:
        """Extract text from PDF using OCR with fallback to PyPDF2."""
        text = ""
        
        try:
            # First try OCR approach for better accuracy
            logger.info("Attempting OCR extraction...")
            
            # Convert PDF pages to images
            pages = convert_from_path(file_path, dpi=300, fmt='jpeg')
            
            for i, page in enumerate(pages):
                logger.debug(f"Processing page {i+1}/{len(pages)} with OCR")
                
                # Use Tesseract to extract text from image
                page_text = pytesseract.image_to_string(page, lang='eng')
                text += page_text + "\n\n"
            
            logger.info(f"OCR extraction successful, extracted {len(text)} characters")
            
        except Exception as ocr_error:
            logger.warning(f"OCR extraction failed: {str(ocr_error)}, falling back to PyPDF2")
            
            try:
                # Fallback to PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                
                logger.info(f"PyPDF2 fallback successful, extracted {len(text)} characters")
                
            except Exception as pypdf_error:
                logger.error(f"Both OCR and PyPDF2 extraction failed: OCR={str(ocr_error)}, PyPDF2={str(pypdf_error)}")
                raise Exception(f"PDF text extraction failed: {str(pypdf_error)}")
        
        return text
    
    # TODO: Implement LinkedIn profile processing
    def process_linkedin_profile(self, url: str, metadata: Dict[str, Any]) -> List[ResourceDocument]:
        """Extract key information from LinkedIn profile."""
        try:
            # Note: LinkedIn has anti-scraping measures, so we'll create a placeholder
            # In a real implementation, you might use LinkedIn API or other methods
            content = f"""
            LinkedIn Profile: {url}
            
            This is Manas Sanjay Pakalapati's professional LinkedIn profile.
            The profile contains information about:
            - Professional experience and work history
            - Educational background
            - Skills and endorsements
            - Professional connections and network
            - Career achievements and milestones
            
            For detailed and up-to-date information, please visit the profile directly.
            """
            
            doc_id = self._generate_doc_id("linkedin", content)
            document = ResourceDocument(
                id=doc_id,
                content=self._clean_text(content),
                source_type="linkedin",
                source_url=url,
                title="LinkedIn Profile",
                description=metadata.get('description', 'LinkedIn professional profile'),
                metadata=metadata,
                created_at=datetime.now()
            )
            
            return [document]
            
        except Exception as e:
            logger.error(f"Error processing LinkedIn profile {url}: {str(e)}")
            return []
    
    # TODO: Implement GitHub profile processing
    def process_github_profile(self, url: str, metadata: Dict[str, Any]) -> List[ResourceDocument]:
        """Extract information from GitHub profile."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract profile information
            profile_name = soup.find('span', {'class': 'p-name'})
            bio = soup.find('div', {'class': 'p-note'})
            
            content = f"GitHub Profile: {url}\n\n"
            
            if profile_name:
                content += f"Profile Name: {profile_name.get_text().strip()}\n"
            
            if bio:
                content += f"Bio: {bio.get_text().strip()}\n"
            
            # Get repository information
            content += "\nThis GitHub profile showcases various projects and repositories including:\n"
            content += "- Software development projects\n"
            content += "- Open source contributions\n"
            content += "- Code samples and demonstrations\n"
            content += "- Technical skills and programming languages used\n"
            
            doc_id = self._generate_doc_id("github_profile", content)
            document = ResourceDocument(
                id=doc_id,
                content=self._clean_text(content),
                source_type="github",
                source_url=url,
                title="GitHub Profile",
                description=metadata.get('description', 'GitHub profile with repositories'),
                metadata=metadata,
                created_at=datetime.now()
            )
            
            return [document]
            
        except Exception as e:
            logger.error(f"Error processing GitHub profile {url}: {str(e)}")
            return []
    
    def process_github_repository(self, url: str, metadata: Dict[str, Any]) -> List[ResourceDocument]:
        """Extract information from a GitHub repository."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract repository information
            repo_name = soup.find('strong', {'itemprop': 'name'})
            description = soup.find('p', {'itemprop': 'about'})
            readme = soup.find('article', {'class': 'markdown-body'})
            
            content = f"GitHub Repository: {url}\n\n"
            
            if repo_name:
                content += f"Repository: {repo_name.get_text().strip()}\n"
            
            if description:
                content += f"Description: {description.get_text().strip()}\n\n"
            
            if readme:
                # Get first few paragraphs of README
                readme_text = readme.get_text()[:1000]  # Limit to first 1000 chars
                content += f"README Summary:\n{readme_text}\n"
            
            doc_id = self._generate_doc_id(f"github_repo_{repo_name}", content)
            document = ResourceDocument(
                id=doc_id,
                content=self._clean_text(content),
                source_type="project",
                source_url=url,
                title=f"GitHub Project: {repo_name.get_text().strip() if repo_name else 'Repository'}",
                description=metadata.get('description', 'GitHub repository'),
                metadata=metadata,
                created_at=datetime.now()
            )
            
            return [document]
            
        except Exception as e:
            logger.error(f"Error processing GitHub repository {url}: {str(e)}")
            return []
    
    def process_medium_article(self, url: str, metadata: Dict[str, Any]) -> List[ResourceDocument]:
        """Extract information from Medium article."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article information
            title = soup.find('h1')
            subtitle = soup.find('h2')
            
            content = f"Medium Article: {url}\n\n"
            
            if title:
                content += f"Title: {title.get_text().strip()}\n"
            
            if subtitle:
                content += f"Subtitle: {subtitle.get_text().strip()}\n\n"
            
            # Extract first few paragraphs
            paragraphs = soup.find_all('p')[:3]  # Get first 3 paragraphs
            for p in paragraphs:
                if p.get_text().strip():
                    content += f"{p.get_text().strip()}\n\n"
            
            content += "This article contains detailed insights and technical content. "
            content += "Visit the link for the complete article."
            
            doc_id = self._generate_doc_id(f"medium_{title}", content)
            document = ResourceDocument(
                id=doc_id,
                content=self._clean_text(content),
                source_type="medium",
                source_url=url,
                title=f"Medium Article: {title.get_text().strip() if title else 'Article'}",
                description=metadata.get('description', 'Medium article'),
                metadata=metadata,
                created_at=datetime.now()
            )
            
            return [document]
            
        except Exception as e:
            logger.error(f"Error processing Medium article {url}: {str(e)}")
            return []
    
    def process_paper_link(self, url: str, metadata: Dict[str, Any]) -> List[ResourceDocument]:
        """Extract information from research paper link."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract paper information (this will vary by platform)
            title = soup.find('title')
            abstract = soup.find('div', {'class': 'abstract'}) or soup.find('p', {'class': 'abstract'})
            
            content = f"Research Paper: {url}\n\n"
            
            if title:
                content += f"Title: {title.get_text().strip()}\n\n"
            
            if abstract:
                content += f"Abstract: {abstract.get_text().strip()}\n\n"
            else:
                content += "This is a research paper or publication by Manas Sanjay Pakalapati. "
                content += "It contains academic research, findings, and technical contributions. "
                content += "Visit the link for the complete paper and detailed information.\n"
            
            doc_id = self._generate_doc_id(f"paper_{title}", content)
            document = ResourceDocument(
                id=doc_id,
                content=self._clean_text(content),
                source_type="paper",
                source_url=url,
                title=f"Research Paper: {title.get_text().strip() if title else 'Publication'}",
                description=metadata.get('description', 'Research paper'),
                metadata=metadata,
                created_at=datetime.now()
            )
            
            return [document]
            
        except Exception as e:
            logger.error(f"Error processing paper link {url}: {str(e)}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        # Remove special characters but keep basic punctuation
        text = ''.join(char for char in text if char.isprintable())
        return text.strip()
    
    def _chunk_text(self, text: str, max_tokens: int = 500) -> List[str]:
        """Split text into chunks based on token count."""
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens = encoding.encode(text)
            
            chunks = []
            for i in range(0, len(tokens), max_tokens):
                chunk_tokens = tokens[i:i + max_tokens]
                chunk_text = encoding.decode(chunk_tokens)
                chunks.append(chunk_text)
            
            return chunks
        except Exception as e:
            logger.error(f"Error chunking text: {str(e)}")
            # Fallback to sentence-based chunking
            sentences = sent_tokenize(text)
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) > max_tokens * 4:  # Rough estimate
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    else:
                        chunks.append(sentence)
                else:
                    current_chunk += " " + sentence
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            return chunks
    
    def _generate_doc_id(self, source: str, content: str) -> str:
        """Generate a unique document ID based on source and content."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{source}_{content_hash}"


class RAGSystem:
    """Main RAG system that orchestrates resource processing and retrieval."""
    
    def __init__(self, resources_dir: str = "resources", db_path: str = "./vector_db"):
        """Initialize the RAG system."""
        self.resources_dir = Path(resources_dir)
        self.db_path = Path(db_path)
        self.processor = ResourceProcessor()
        
        # Initialize embedding model
        logger.info("Loading sentence transformer model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.db_path.mkdir(exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="portfolio_resources",
            metadata={"description": "Manas Sanjay Pakalapati's portfolio resources"}
        )
        
        logger.info("RAG system initialized successfully")
    
    def load_resources_config(self) -> Dict[str, Any]:
        """Load resources configuration from YAML file."""
        config_path = self.resources_dir / "resources.yaml"
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Loaded resources config from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading resources config: {str(e)}")
            return {}
    
    def process_all_resources(self) -> bool:
        """Process all resources and update the vector database."""
        try:
            config = self.load_resources_config()
            if not config or 'resources' not in config:
                logger.error("Invalid or empty resources configuration")
                return False
            
            resources = config['resources']
            all_documents = []
            
            # Process resume
            if 'resume' in resources:
                resume_config = resources['resume']
                resume_path = self.resources_dir / resume_config['path']
                if resume_path.exists():
                    logger.info(f"Processing resume: {resume_path}")
                    docs = self.processor.process_pdf(str(resume_path), resume_config)
                    all_documents.extend(docs)
            
            # Process profiles
            if 'profiles' in resources:
                for profile_name, profile_config in resources['profiles'].items():
                    if 'url' in profile_config:
                        logger.info(f"Processing {profile_name} profile: {profile_config['url']}")
                        if profile_name == 'linkedin':
                            docs = self.processor.process_linkedin_profile(
                                profile_config['url'], profile_config
                            )
                        elif profile_name == 'github':
                            docs = self.processor.process_github_profile(
                                profile_config['url'], profile_config
                            )
                        else:
                            continue  # Skip unknown profile types
                        all_documents.extend(docs)
            
            # Process project repositories
            if 'projects' in resources and 'github_repos' in resources['projects']:
                for repo_config in resources['projects']['github_repos']:
                    if isinstance(repo_config, dict) and 'url' in repo_config:
                        logger.info(f"Processing GitHub repo: {repo_config['url']}")
                        docs = self.processor.process_github_repository(
                            repo_config['url'], repo_config
                        )
                        all_documents.extend(docs)
            
            # Store documents in vector database
            if all_documents:
                self._store_documents(all_documents)
                logger.info(f"Successfully processed and stored {len(all_documents)} documents")
                return True
            else:
                logger.warning("No documents were processed")
                return False
                
        except Exception as e:
            logger.error(f"Error processing resources: {str(e)}")
            return False
    
    def _store_documents(self, documents: List[ResourceDocument]) -> None:
        """Store documents in the vector database."""
        try:
            # Prepare data for ChromaDB
            ids = []
            embeddings = []
            metadatas = []
            documents_text = []
            
            for doc in documents:
                ids.append(doc.id)
                documents_text.append(doc.content)
                
                # Generate embedding
                embedding = self.embedding_model.encode(doc.content).tolist()
                embeddings.append(embedding)
                
                # Prepare metadata
                metadata = {
                    'source_type': doc.source_type,
                    'source_url': doc.source_url or '',
                    'title': doc.title,
                    'description': doc.description,
                    'created_at': doc.created_at.isoformat(),
                    'chunk_index': doc.chunk_index or 0,
                    **doc.metadata
                }
                metadatas.append(metadata)
            
            # Store in ChromaDB (upsert to handle updates)
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents_text
            )
            
            logger.info(f"Stored {len(documents)} documents in vector database")
            
        except Exception as e:
            logger.error(f"Error storing documents: {str(e)}")
            raise
    
    def retrieve_context(self, query: str, max_results: int = 5) -> List[RetrievalResult]:
        """Retrieve relevant context for a given query."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=max_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Process results
            retrieval_results = []
            for i, (doc_text, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                # Convert distance to similarity score
                score = 1.0 - distance
                
                # Reconstruct document
                document = ResourceDocument(
                    id=results['ids'][0][i],
                    content=doc_text,
                    source_type=metadata['source_type'],
                    source_url=metadata.get('source_url'),
                    title=metadata['title'],
                    description=metadata['description'],
                    metadata=metadata,
                    created_at=datetime.fromisoformat(metadata['created_at']),
                    chunk_index=metadata.get('chunk_index')
                )
                
                retrieval_results.append(RetrievalResult(
                    document=document,
                    score=score,
                    rank=i + 1
                ))
            
            logger.info(f"Retrieved {len(retrieval_results)} relevant documents for query")
            return retrieval_results
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []
    
    def format_context_with_citations(self, retrieval_results: List[RetrievalResult]) -> Tuple[str, List[str]]:
        """Format retrieved context with citations."""
        context_parts = []
        citations = []
        
        for result in retrieval_results:
            doc = result.document
            
            # Add content to context
            context_parts.append(f"[Source: {doc.title}]\n{doc.content}")
            
            # Add citation
            if doc.source_url:
                citations.append(f"- {doc.title}: {doc.source_url}")
            else:
                citations.append(f"- {doc.title}")
        
        context = "\n\n".join(context_parts)
        return context, citations
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector database."""
        try:
            count = self.collection.count()
            
            # Get sample of documents to analyze types
            sample_results = self.collection.get(limit=100, include=['metadatas'])
            source_types = {}
            
            for metadata in sample_results['metadatas']:
                source_type = metadata.get('source_type', 'unknown')
                source_types[source_type] = source_types.get(source_type, 0) + 1
            
            return {
                'total_documents': count,
                'source_types': source_types,
                'database_path': str(self.db_path)
            }
            
        except Exception as e:
            logger.error(f"Error getting database stats: {str(e)}")
            return {'error': str(e)}
