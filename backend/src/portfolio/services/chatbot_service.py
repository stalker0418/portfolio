"""Main chatbot service that integrates AI models and resources."""

import time
from typing import Dict, Any, Optional
from src.portfolio.services.ai_models import AIModelService
from src.portfolio.services.resource_manager import ResourceManager
from config.settings import settings


class ChatbotService:
    """Main chatbot service integrating AI models and resources."""
    
    def __init__(self):
        self.ai_service = AIModelService()
        self.resource_manager = ResourceManager()
        self.is_initialized = False
    
    async def initialize(self) -> None:
        """Initialize the chatbot service."""
        try:
            # Initialize AI models
            await self.ai_service.initialize()
            
            # Load resources
            await self.resource_manager.load_resources()
            
            self.is_initialized = True
            print("✅ Chatbot service initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize chatbot service: {e}")
            raise
    
    async def get_response(self, message: str, model_provider: Optional[str] = None) -> Dict[str, Any]:
        """Get response from the chatbot."""
        if not self.is_initialized:
            raise RuntimeError("Chatbot service not initialized")
        
        start_time = time.time()
        
        try:
            # Create enhanced prompt with resource context
            enhanced_prompt = self._create_enhanced_prompt(message)
            
            # Get response from AI service
            response = await self.ai_service.get_response(
                prompt=enhanced_prompt,
                provider=model_provider
            )
            
            # Add processing time
            processing_time = time.time() - start_time
            response["processing_time"] = processing_time
            
            return response
            
        except Exception as e:
            print(f"Error in chatbot service: {e}")
            raise
    
    def _create_enhanced_prompt(self, user_message: str) -> str:
        """Create an enhanced prompt with resource context."""
        base_prompt = f"""You are an AI assistant representing Manas Sanjay Pakalapati's portfolio. 
You have access to his professional information and resources.

Available Resources:
{self.resource_manager.get_resource_summary()}

User Question: {user_message}

Please provide a helpful and accurate response based on Manas's portfolio information. 
If you don't have specific information about something, please say so clearly.
Be professional, friendly, and informative in your responses."""

        return base_prompt
    
    async def get_portfolio_summary(self) -> str:
        """Get a summary of the portfolio."""
        if not self.is_initialized:
            raise RuntimeError("Chatbot service not initialized")
        
        try:
            summary_prompt = """Please provide a comprehensive summary of Manas Sanjay Pakalapati's portfolio, 
including his professional background, skills, projects, and achievements. 
Base this on the available resources and information."""
            
            response = await self.ai_service.get_response(summary_prompt)
            return response["answer"]
            
        except Exception as e:
            print(f"Error getting portfolio summary: {e}")
            return "Unable to generate portfolio summary at this time."
    
    async def close(self) -> None:
        """Close the chatbot service."""
        await self.ai_service.close()
        self.is_initialized = False
