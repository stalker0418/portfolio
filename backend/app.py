"""
Simple FastAPI backend for Manas's portfolio with chatbot functionality.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime
from dotenv import load_dotenv

# Import chatbot from separate module
from chatbot import ChatbotWrapper, ChatMessage
from rag import get_rag_system, initialize_knowledge_base

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Manas Portfolio Backend",
    description="AI-powered portfolio backend with chatbot functionality",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Create React App default
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://127.0.0.1:5173",  # Alternative localhost
        "https://manas-portfolio-backend.fly.dev",  # Your Fly.io backend (for health checks)
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # All Vercel deployment domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Pydantic models for API requests/responses
class ChatRequest(BaseModel):
    message: str
    model_name: Optional[str] = None  # Allow frontend to specify model
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    response: str
    model_used: str
    timestamp: datetime


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str


class RAGStatusResponse(BaseModel):
    status: str
    collection_info: dict
    timestamp: datetime


# Initialize chatbot
chatbot = ChatbotWrapper()


# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health status check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that connects to the frontend chat interface.
    Receives messages from frontend and returns AI responses.
    """
    try:
        logger.info(f"Received chat request: {request.message}")
        
        # Get response from chatbot
        response = await chatbot.chat(
            message=request.message,
            model_name=request.model_name,  # Use model from request or default
            conversation_history=request.conversation_history
        )
        
        # Determine which model was actually used
        actual_model = request.model_name or chatbot.default_model
        
        return ChatResponse(
            response=response,
            model_used=actual_model,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rag/status", response_model=RAGStatusResponse)
async def rag_status():
    """Get RAG system status and collection information."""
    try:
        rag = get_rag_system()
        collection_info = rag.get_collection_info()
        
        return RAGStatusResponse(
            status="active",
            collection_info=collection_info,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"RAG status check error: {str(e)}")
        return RAGStatusResponse(
            status="error",
            collection_info={"error": str(e)},
            timestamp=datetime.now()
        )


@app.post("/rag/initialize")
async def initialize_rag():
    """Initialize or reinitialize the RAG knowledge base."""
    try:
        success = initialize_knowledge_base("./resources/knowledge.md")
        if success:
            return {"status": "success", "message": "Knowledge base initialized successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize knowledge base")
    except Exception as e:
        logger.error(f"RAG initialization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "message": "Manas Portfolio Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "rag/status": "/rag/status",
            "rag/initialize": "/rag/initialize",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

