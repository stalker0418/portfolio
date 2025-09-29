"""
Chatbot module for AI-powered chat functionality.
Supports multiple AI providers: OpenAI, Anthropic, TogetherAI
"""
from typing import List, Optional
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import os
from together import Together
import PyPDF2
import yaml

# Configure logging
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatbotWrapper:
    """
    AI Chatbot wrapper that supports multiple providers.
    Currently supports: OpenAI, Anthropic, TogetherAI
    """
    
    def __init__(self):
        self.default_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
        
        # Initialize Together AI client
        try:
            self.together_client = Together()
            logger.info("Together AI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Together AI client: {str(e)}")
            self.together_client = None
        
        # Load resume content
        self.resume_content = self._load_resume_content()
        
    def _load_resume_content(self) -> str:
        """Load and extract text content from the resume PDF."""
        try:
            # Get the path to the resume
            resources_dir = os.path.join(os.path.dirname(__file__), "resources")
            
            # Load resources.yaml to get resume path
            resources_file = os.path.join(resources_dir, "resources.yaml")
            if os.path.exists(resources_file):
                with open(resources_file, 'r') as f:
                    resources_data = yaml.safe_load(f)
                    resume_path = resources_data.get('resources', {}).get('resume', {}).get('path', 'Manas_Sanjay_Pakalapati_Resume.pdf')
            else:
                resume_path = 'Manas_Sanjay_Pakalapati_Resume.pdf'
            
            # Full path to resume
            full_resume_path = os.path.join(resources_dir, resume_path)
            
            if not os.path.exists(full_resume_path):
                logger.warning(f"Resume PDF not found at {full_resume_path}")
                return "Resume content not available."
            
            # Extract text from PDF
            with open(full_resume_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text_content = []
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content.append(page.extract_text())
                
                resume_text = '\n'.join(text_content)
                
                # Limit resume content to avoid long API calls (keep first 2000 chars for key info)
                if len(resume_text) > 2000:
                    resume_text = resume_text[:2000] + "\n\n[Resume content truncated for performance]"
                
                logger.info(f"Successfully extracted {len(resume_text)} characters from resume PDF")
                return resume_text
                
        except Exception as e:
            logger.error(f"Error loading resume content: {str(e)}")
            return "Resume content could not be loaded due to an error."
    
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
        Send a chat message and get response from the specified AI model.
        """
        # Use default model if none specified
        if model_name is None:
            model_name = self.default_model
            
        provider = self._get_provider_from_model(model_name)
        
        # Handle None conversation_history
        if conversation_history is None:
            conversation_history = []
        
        try:
            if provider == "togetherai":
                return await self._chat_togetherai(message, model_name, conversation_history)
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
        conversation_history: List[ChatMessage]
    ) -> str:
        """
        TogetherAI implementation using the Together AI SDK.
        """
        if not self.together_client:
            raise HTTPException(
                status_code=500, 
                detail="Together AI client not initialized. Check your API key."
            )
        
        try:
            # Build messages array from conversation history
            messages = []
            
            # Add system message for context with actual resume content
            system_prompt = f"""You are Manas's AI assistant on his portfolio website. You have access to his complete resume and should answer questions based ONLY on the factual information provided below. Be helpful, professional, and engaging.

IMPORTANT: Base your answers strictly on the resume content provided. Do not make up or assume information not present in the resume.

=== MANAS'S RESUME CONTENT ===
{self.resume_content}
=== END OF RESUME CONTENT ===

Instructions:
- Answer questions about Manas's experience, skills, education, and projects based on the resume above
- If asked about something not mentioned in the resume, politely say you don't have that information
- Be conversational but accurate
- Always be on point and on the side of Manas. Try to be as concise and helpful as possible
- If you don't know the answer, say you don't know. Don't make up an answer.
"""
            
            messages.append({
                "role": "system",
                "content": system_prompt
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
            
            # Make API call to Together AI with timeout
            response = self.together_client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=500,  # Reduced for faster responses
                temperature=0.7,
                stream=False,  # Ensure we get a complete response, not streaming
                # Note: Together API doesn't support timeout parameter directly
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
