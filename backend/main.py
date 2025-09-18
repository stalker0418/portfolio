from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import asyncio
from chatbot.rag_system import RAGChatbot

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Manas Sanjay Portfolio API",
    description="AI-powered portfolio backend with RAG chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://manas-sanjay-pakalapati-portfolio.vercel.app",
        "https://*.vercel.app"  # Allow any Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG chatbot
chatbot = RAGChatbot()

# Pydantic models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    confidence: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    message: str

@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot on startup"""
    try:
        await chatbot.initialize()
        print("✅ RAG Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Manas Sanjay Portfolio API is running!"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return HealthResponse(
        status="healthy",
        message="All systems operational"
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """
    Chat with the AI assistant about Manas Sanjay's portfolio
    """
    try:
        if not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get response from RAG chatbot
        response = await chatbot.get_response(message.message)
        
        return ChatResponse(
            response=response["answer"],
            confidence=response.get("confidence")
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="I'm having trouble processing your request. Please try again."
        )

@app.get("/api/portfolio/summary")
async def get_portfolio_summary():
    """Get a summary of Manas's portfolio"""
    try:
        summary = await chatbot.get_portfolio_summary()
        return {"summary": summary}
    except Exception as e:
        print(f"Error getting portfolio summary: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch portfolio summary")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
