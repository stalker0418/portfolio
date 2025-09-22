"""
Chatbot module for AI-powered chat functionality with RAG support.
Supports multiple AI providers: OpenAI, Anthropic, TogetherAI
Includes Retrieval-Augmented Generation (RAG) for contextual responses.
"""
from typing import List, Optional
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import os
from together import Together

# Import RAG system
from rag_system import RAGSystem

# Configure logging
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatbotWrapper:
    """
    AI Chatbot wrapper that supports multiple providers with RAG capabilities.
    Currently supports: OpenAI, Anthropic, TogetherAI
    Includes Retrieval-Augmented Generation for contextual responses.
    """
    
    def __init__(self, enable_rag: bool = True):
        self.default_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
        self.enable_rag = enable_rag
        
        # Initialize Together AI client
        try:
            self.together_client = Together()
            logger.info("Together AI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Together AI client: {str(e)}")
            self.together_client = None
        
        # Initialize RAG system
        if self.enable_rag:
            try:
                self.rag_system = RAGSystem()
                logger.info("RAG system initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize RAG system: {str(e)}")
                self.rag_system = None
                self.enable_rag = False
        else:
            self.rag_system = None
    
    def _get_provider_from_model(self, model_name: str) -> str:
        """Determine which provider to use based on model name patterns."""
        model_name_lower = model_name.lower()
        
        # Check for OpenAI models (contains 'gpt')
        if 'gpt' in model_name_lower:
            return "openai"
        
        # Check for Anthropic models (contains 'claude')
        if 'claude' in model_name_lower:
            return "anthropic"
        
        # Default to TogetherAI for all other models
        return "togetherai"
    
    async def chat(
        self, 
        message: str, 
        model_name: Optional[str] = None, 
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> str:
        """
        Send a chat message and get response from the specified AI model with RAG support.
        """
        # Use default model if none specified
        if model_name is None:
            model_name = self.default_model
            
        provider = self._get_provider_from_model(model_name)
        
        # Handle None conversation_history
        if conversation_history is None:
            conversation_history = []
        
        # Get relevant context using RAG if enabled
        context = ""
        citations = []
        if self.enable_rag and self.rag_system:
            try:
                retrieval_results = self.rag_system.retrieve_context(message, max_results=3)
                if retrieval_results:
                    context, citations = self.rag_system.format_context_with_citations(retrieval_results)
                    logger.info(f"Retrieved context from {len(retrieval_results)} sources")
            except Exception as e:
                logger.warning(f"Failed to retrieve RAG context: {str(e)}")
        
        try:
            if provider == "togetherai":
                response = await self._chat_togetherai(message, model_name, conversation_history, context)
                # Add citations to response if available
                if citations:
                    response += "\n\n**Sources:**\n" + "\n".join(citations)
                return response
            elif provider == "openai":
                # TODO: Implement OpenAI integration
                return "OpenAI integration coming soon! This is a placeholder response."
            elif provider == "anthropic":
                # TODO: Implement Anthropic integration
                return "Anthropic integration coming soon! This is a placeholder response."
            else:
                raise ValueError(f"Unsupported model provider: {provider}")
                
        except Exception as e:
            logger.error(f"Error in chat with {provider}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
    
    async def _chat_togetherai(
        self, 
        message: str, 
        model_name: str, 
        conversation_history: List[ChatMessage],
        context: str = ""
    ) -> str:
        """
        TogetherAI implementation using the Together AI SDK with RAG context.
        """
        if not self.together_client:
            raise HTTPException(
                status_code=500, 
                detail="Together AI client not initialized. Check your API key."
            )
        
        try:
            # Build messages array from conversation history
            messages = []
            
            # Build enhanced system message with context
            system_message = """You are Manas Sanjay Pakalapati's AI assistant on his portfolio website. You are knowledgeable about his background, skills, and projects. Be helpful, professional, and engaging.

When answering questions, use the provided context information to give accurate and specific responses about Manas's experience, skills, projects, and background. Always be truthful and if you don't have specific information, say so."""

            if context:
                system_message += f"\n\nRelevant Context Information:\n{context}\n\nUse this context to provide specific and accurate information about Manas's background, experience, and projects."
            
            messages.append({
                "role": "system",
                "content": system_message
            })
            
            # Add conversation history
            for chat_msg in conversation_history:
                messages.append({
                    "role": chat_msg.role,
                    "content": chat_msg.content
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": message
            })
            
            logger.info(f"Sending request to Together AI with model: {model_name}")
            logger.debug(f"Messages: {messages}")
            
            # Make API call to Together AI
            response = self.together_client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                stream=False  # Ensure we get a complete response, not streaming
            )
            
            # Extract response content
            try:
                if hasattr(response, 'choices') and response.choices and len(response.choices) > 0:  # type: ignore
                    choice = response.choices[0]  # type: ignore
                    if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                        response_content = str(choice.message.content)  # type: ignore
                        logger.info(f"Received response from Together AI: {response_content[:100]}...")
                        return response_content
                
                # Fallback: try to extract content from response directly
                response_str = str(response)
                logger.warning(f"Unexpected response format: {response_str[:200]}...")
                return f"Received response but couldn't parse properly. Raw response: {response_str}"
                
            except Exception as parse_error:
                logger.error(f"Error parsing Together AI response: {str(parse_error)}")
                return f"Sorry, I received a response but couldn't parse it properly. Error: {str(parse_error)}"
                
        except Exception as e:
            logger.error(f"Error in Together AI chat: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Together AI error: {str(e)}"
            )
