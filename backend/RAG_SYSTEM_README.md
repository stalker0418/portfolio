# RAG System Implementation for Portfolio Chatbot

## Overview

This document describes the comprehensive Retrieval-Augmented Generation (RAG) system implemented for Manas Sanjay Pakalapati's portfolio chatbot. The system enables the chatbot to provide contextually accurate responses about Manas's background, skills, projects, and experience by retrieving relevant information from various resources.

## Architecture

### Components

1. **RAGSystem** (`rag_system.py`): Main orchestrator
2. **ResourceProcessor**: Handles different resource types
3. **ChromaDB**: Free vector database for storing embeddings
4. **SentenceTransformers**: For generating embeddings
5. **ChatbotWrapper**: Enhanced with RAG capabilities

### Supported Resource Types

| Type | Description | Processing Method |
|------|-------------|-------------------|
| **Resume (PDF)** | Professional resume | Text extraction + chunking |
| **LinkedIn Profile** | Professional profile link | Metadata extraction |
| **GitHub Profile** | Developer profile | Profile info + repository overview |
| **GitHub Repositories** | Project repositories | README + description extraction |
| **Medium Articles** | Blog posts and articles | Title + summary extraction |
| **Research Papers** | Academic publications | Title + abstract extraction |

## Key Features

### 1. Intelligent Resource Processing
- **OCR PDF Processing**: Uses Tesseract OCR for superior text extraction from resume PDFs with PyPDF2 fallback
- **Web Scraping**: BeautifulSoup for extracting key information from web pages
- **Smart Chunking**: Token-based text chunking for optimal context retrieval
- **Metadata Preservation**: Maintains source URLs and descriptions for citations

### 2. Vector Database Storage
- **ChromaDB Integration**: Free, persistent vector database
- **Embedding Generation**: Uses `all-MiniLM-L6-v2` model for semantic embeddings
- **Efficient Retrieval**: Similarity search for relevant context

### 3. Context-Aware Chatbot
- **RAG Integration**: Retrieves relevant context for each user query
- **Citation System**: Automatically includes source links in responses
- **Enhanced System Prompts**: Context-aware prompts for accurate responses

### 4. Deployment Automation
- **Automatic Database Updates**: RAG database updates automatically during Fly.io deployment
- **OCR System Dependencies**: Tesseract and Poppler automatically installed in Docker container
- **API Endpoints**: REST endpoints for database management
- **Persistent Storage**: Vector database persisted across deployments using Fly.io volumes
- **Startup Integration**: Automatic database initialization and updates on deployment

## File Structure

```
backend/
├── rag_system.py              # Main RAG system implementation (with OCR)
├── chatbot.py                 # Enhanced chatbot with RAG support
├── app.py                     # FastAPI app with RAG endpoints
├── update_rag_database.py     # Database update script
├── startup.py                 # Deployment startup script (auto RAG update)
├── test_rag.py               # Test suite for RAG system
├── test_ocr.py               # OCR functionality test script
├── Dockerfile                 # Docker config with OCR dependencies
├── fly.toml                   # Fly.io deployment config with volume mounts
├── DEPLOYMENT_GUIDE.md        # Complete deployment guide
├── resources/
│   ├── resources.yaml         # Resource configuration
│   └── Manas_Sanjay_Pakalapati_Resume.pdf
└── vector_db/                 # ChromaDB storage (persistent via Fly.io volume)
```

## Configuration

### Environment Variables

```bash
# RAG System Configuration
ENABLE_RAG=true
VECTOR_DB_PATH="./vector_db"
CHUNK_SIZE=500
CHUNK_OVERLAP=100
EMBEDDING_MODEL="all-MiniLM-L6-v2"
MAX_RETRIEVAL_RESULTS=3

# Resource Configuration
RESOURCES_DIR="resources"
RESOURCES_CONFIG_FILE="resources.yaml"
```

### Dependencies Added

```toml
# RAG System Dependencies
"chromadb>=0.4.0",           # Vector database
"sentence-transformers>=2.2.0",  # Embeddings
"pypdf2>=3.0.0",            # PDF processing fallback
"pdf2image>=1.16.0",        # PDF to image conversion for OCR
"pytesseract>=0.3.10",      # OCR engine Python wrapper
"pillow>=9.5.0",            # Image processing
"beautifulsoup4>=4.12.0",   # Web scraping
"lxml>=4.9.0",              # XML/HTML parsing
"nltk>=3.8.0",              # Natural language processing
"tiktoken>=0.5.0",          # Token counting
```

### System Dependencies (Auto-installed in Docker)

```bash
# OCR and PDF processing
tesseract-ocr              # OCR engine
tesseract-ocr-eng          # English language pack
poppler-utils              # PDF utilities
libgl1-mesa-glx           # OpenGL support
libglib2.0-0              # GLib library
```

## Usage

### 1. Local Development Setup

```bash
# Install dependencies (including OCR)
pip install -e .

# Install system dependencies (macOS)
brew install tesseract poppler

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install tesseract-ocr tesseract-ocr-eng poppler-utils

# Test OCR functionality
python test_ocr.py

# Update RAG database
python update_rag_database.py --verbose --stats
```

### 2. Testing the System

```bash
# Test OCR and PDF processing
python test_ocr.py

# Run comprehensive RAG tests
python test_rag.py
```

### 3. Local Development Server

```bash
# Start with RAG database update
python startup.py

# Or start normally (RAG will initialize automatically)
python app.py

# Skip RAG update for faster startup during development
SKIP_RAG_UPDATE=true python startup.py
```

### 4. Production Deployment (Fly.io)

```bash
# Deploy with automatic RAG database update
flyctl deploy

# The deployment will automatically:
# 1. Install OCR dependencies in Docker
# 2. Update RAG database with latest resources
# 3. Start the server with enhanced context

# See DEPLOYMENT_GUIDE.md for detailed instructions
```

### 4. API Endpoints

#### Update RAG Database
```bash
POST /rag/update
```
Processes all resources and updates the vector database.

#### Get Database Statistics
```bash
GET /rag/stats
```
Returns database statistics including document counts by type.

#### Enhanced Chat
```bash
POST /chat
```
Now includes RAG context retrieval and citations in responses.

## How It Works

### 1. Resource Processing Flow

```
resources.yaml → ResourceProcessor → Text Extraction → Chunking → Embeddings → ChromaDB
```

1. **Configuration Loading**: Reads `resources.yaml` for resource definitions
2. **Resource Processing**: Each resource type has a specialized processor
3. **Text Extraction**: Extracts relevant text content
4. **Chunking**: Splits content into manageable chunks (500 tokens)
5. **Embedding Generation**: Creates semantic embeddings using SentenceTransformers
6. **Storage**: Stores embeddings and metadata in ChromaDB

### 2. Query Processing Flow

```
User Query → Embedding → Similarity Search → Context Retrieval → Enhanced Prompt → AI Response → Citations
```

1. **Query Embedding**: Converts user query to vector embedding
2. **Similarity Search**: Finds most relevant document chunks
3. **Context Assembly**: Combines relevant chunks with metadata
4. **Enhanced Prompting**: Adds context to system prompt
5. **AI Generation**: Generates response using context
6. **Citation Addition**: Appends source links to response

### 3. Example Resource Processing

#### Resume (PDF)
```python
# Extract text from PDF
pdf_text = extract_pdf_text("resume.pdf")

# Split into chunks
chunks = chunk_text(pdf_text, max_tokens=500)

# Create documents with metadata
for chunk in chunks:
    document = ResourceDocument(
        content=chunk,
        source_type="resume",
        title="Resume - Section X",
        metadata={"chunk_index": i}
    )
```

#### GitHub Repository
```python
# Scrape repository information
repo_info = scrape_github_repo(url)

# Extract key information
content = f"""
Repository: {repo_info.name}
Description: {repo_info.description}
README: {repo_info.readme_summary}
"""

# Store as single document
document = ResourceDocument(
    content=content,
    source_type="project",
    source_url=url,
    title=f"GitHub Project: {repo_info.name}"
)
```

## Deployment

### 1. Automatic Database Updates

The system includes several mechanisms for keeping the database updated:

#### During Deployment
```python
# startup.py automatically runs database update
python startup.py
```

#### Manual Updates
```bash
# Command line script
python update_rag_database.py --force --verbose

# API endpoint
curl -X POST http://localhost:8000/rag/update
```

#### Scheduled Updates
```bash
# Add to crontab for daily updates
0 2 * * * cd /path/to/backend && python update_rag_database.py
```

### 2. Production Considerations

- **API Keys**: Ensure Together AI API key is set
- **Database Persistence**: Vector database is stored locally in `./vector_db`
- **Resource Updates**: Update `resources.yaml` when adding new resources
- **Monitoring**: Use `/rag/stats` endpoint to monitor database health

## Example Interactions

### Before RAG Implementation
```
User: "What are your technical skills?"
Bot: "I'm an AI assistant. I can help you with various tasks."
```

### After RAG Implementation
```
User: "What are your technical skills?"
Bot: "Based on my resume and experience, I have expertise in:

- Programming Languages: Python, JavaScript, TypeScript, Java
- Web Technologies: React, Node.js, FastAPI, HTML/CSS
- Databases: PostgreSQL, MongoDB, ChromaDB
- Cloud Platforms: AWS, Google Cloud
- Machine Learning: TensorFlow, PyTorch, Scikit-learn

**Sources:**
- Resume: /path/to/resume
- GitHub Profile: https://github.com/manassanjay
```

## Benefits

1. **Accurate Information**: Responses based on actual resume and project data
2. **Source Attribution**: Every response includes relevant links
3. **Scalable**: Easy to add new resource types and sources
4. **Maintainable**: Automatic updates when resources change
5. **Cost-Effective**: Uses free ChromaDB instead of paid vector databases

## Future Enhancements

1. **Real-time Updates**: Webhook-based updates when resources change
2. **Advanced Scraping**: More sophisticated web scraping for dynamic content
3. **Multi-modal Support**: Image and document analysis
4. **Conversation Memory**: Persistent conversation context
5. **Analytics**: Track popular queries and improve responses

## Troubleshooting

### Common Issues

1. **ChromaDB Initialization Error**
   ```bash
   # Clear database and rebuild
   rm -rf vector_db/
   python update_rag_database.py --force
   ```

2. **PDF Processing Error**
   ```bash
   # Check PDF file exists and is readable
   ls -la resources/Manas_Sanjay_Pakalapati_Resume.pdf
   ```

3. **Web Scraping Failures**
   ```bash
   # Check internet connectivity and URL accessibility
   curl -I https://github.com/manassanjay
   ```

4. **Missing Dependencies**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

### Debugging

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Use the test script:
```bash
python test_rag.py
```

Check database statistics:
```bash
curl http://localhost:8000/rag/stats
```

## Conclusion

The RAG system transforms the portfolio chatbot from a generic AI assistant into a knowledgeable representative that can provide accurate, contextual information about Manas's background, skills, and projects. The system is designed to be maintainable, scalable, and easy to deploy, making it an ideal solution for an AI-powered portfolio website.
