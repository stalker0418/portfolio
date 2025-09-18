"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.portfolio.api import chat, health
from src.portfolio.services.chatbot_service import ChatbotService
from config.settings import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot service instance
chatbot_service = ChatbotService()


@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot service on startup."""
    try:
        await chatbot_service.initialize()
        
        # Inject the service into the dependency
        chat.get_chatbot_service._instance = chatbot_service
        
        print("✅ Portfolio API initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize API: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    try:
        await chatbot_service.close()
        print("✅ Portfolio API shutdown complete")
    except Exception as e:
        print(f"❌ Error during shutdown: {e}")


# Include routers
app.include_router(health.router)
app.include_router(chat.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug,
        log_level="info"
    )
