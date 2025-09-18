"""Chat API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from src.portfolio.models.chat import ChatMessage, ChatResponse, PortfolioSummary
from src.portfolio.services.chatbot_service import ChatbotService
from typing import Optional

router = APIRouter(prefix="/api/chat", tags=["chat"])


async def get_chatbot_service() -> ChatbotService:
    """Dependency to get chatbot service instance."""
    # This will be injected by the main app
    return getattr(get_chatbot_service, '_instance', None)


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    message: ChatMessage,
    chatbot_service: ChatbotService = Depends(get_chatbot_service)
):
    """
    Chat with the AI assistant about Manas Sanjay's portfolio.
    """
    try:
        if not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get response from chatbot service
        response = await chatbot_service.get_response(
            message=message.message,
            model_provider=message.model_provider.value if message.model_provider else None
        )
        
        return ChatResponse(
            response=response["answer"],
            confidence=response.get("confidence"),
            model_used=response.get("provider"),
            processing_time=response.get("processing_time")
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="I'm having trouble processing your request. Please try again."
        )


@router.get("/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(
    chatbot_service: ChatbotService = Depends(get_chatbot_service)
):
    """Get a summary of Manas's portfolio."""
    try:
        summary = await chatbot_service.get_portfolio_summary()
        return PortfolioSummary(summary=summary)
    except Exception as e:
        print(f"Error getting portfolio summary: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch portfolio summary")
