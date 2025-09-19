"""AI model service layer for different providers."""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import httpx
from config.simple_settings import settings


class AIModelProvider(ABC):
    """Abstract base class for AI model providers."""
    
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the model provider."""
        pass
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the model."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the model provider."""
        pass


class TogetherAIProvider(AIModelProvider):
    """TogetherAI model provider."""
    
    def __init__(self, api_key: str, model_name: str = "meta-llama/Llama-2-7b-chat-hf"):
        super().__init__(api_key, model_name)
        self.base_url = "https://api.together.xyz/v1"
    
    async def initialize(self) -> None:
        """Initialize TogetherAI client."""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response using TogetherAI API."""
        if not self.client:
            await self.initialize()
        
        # TogetherAI uses the same format as OpenAI for chat completions
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": kwargs.get("max_tokens", settings.model_max_tokens),
            "temperature": kwargs.get("temperature", settings.model_temperature),
            "top_p": kwargs.get("top_p", 0.9),
            "stop": kwargs.get("stop", ["</s>", "Human:", "Assistant:"])
        }
        
        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            
            return {
                "answer": data["choices"][0]["message"]["content"].strip(),
                "confidence": 0.8,  # TogetherAI doesn't provide confidence scores
                "model_used": self.model_name,
                "provider": "together"
            }
        except httpx.HTTPError as e:
            raise Exception(f"TogetherAI API error: {e}")
    
    async def close(self) -> None:
        """Close the TogetherAI client."""
        if self.client:
            await self.client.aclose()


class OpenAIProvider(AIModelProvider):
    """OpenAI model provider."""
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model_name)
        self.base_url = "https://api.openai.com/v1"
    
    async def initialize(self) -> None:
        """Initialize OpenAI client."""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response using OpenAI API."""
        if not self.client:
            await self.initialize()
        
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", settings.model_max_tokens),
            "temperature": kwargs.get("temperature", settings.model_temperature),
            "top_p": kwargs.get("top_p", 1.0)
        }
        
        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            
            return {
                "answer": data["choices"][0]["message"]["content"].strip(),
                "confidence": 0.9,  # OpenAI provides more reliable responses
                "model_used": self.model_name,
                "provider": "openai"
            }
        except httpx.HTTPError as e:
            raise Exception(f"OpenAI API error: {e}")
    
    async def close(self) -> None:
        """Close the OpenAI client."""
        if self.client:
            await self.client.aclose()


class AnthropicProvider(AIModelProvider):
    """Anthropic model provider."""
    
    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229"):
        super().__init__(api_key, model_name)
        self.base_url = "https://api.anthropic.com/v1"
    
    async def initialize(self) -> None:
        """Initialize Anthropic client."""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            timeout=30.0
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response using Anthropic API."""
        if not self.client:
            await self.initialize()
        
        payload = {
            "model": self.model_name,
            "max_tokens": kwargs.get("max_tokens", settings.model_max_tokens),
            "temperature": kwargs.get("temperature", settings.model_temperature),
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = await self.client.post("/messages", json=payload)
            response.raise_for_status()
            data = response.json()
            
            return {
                "answer": data["content"][0]["text"].strip(),
                "confidence": 0.85,  # Anthropic provides high-quality responses
                "model_used": self.model_name,
                "provider": "anthropic"
            }
        except httpx.HTTPError as e:
            raise Exception(f"Anthropic API error: {e}")
    
    async def close(self) -> None:
        """Close the Anthropic client."""
        if self.client:
            await self.client.aclose()


class AIModelService:
    """Service for managing AI model providers."""
    
    def __init__(self):
        self.providers: Dict[str, AIModelProvider] = {}
        self.default_provider: Optional[str] = None
    
    async def initialize(self) -> None:
        """Initialize all available model providers."""
        # Initialize TogetherAI if API key is available
        if settings.together_api_key:
            together_provider = TogetherAIProvider(settings.together_api_key)
            await together_provider.initialize()
            self.providers["together"] = together_provider
        
        # Initialize OpenAI if API key is available
        if settings.openai_api_key:
            openai_provider = OpenAIProvider(settings.openai_api_key)
            await openai_provider.initialize()
            self.providers["openai"] = openai_provider
        
        # Initialize Anthropic if API key is available
        if settings.anthropic_api_key:
            anthropic_provider = AnthropicProvider(settings.anthropic_api_key)
            await anthropic_provider.initialize()
            self.providers["anthropic"] = anthropic_provider
        
        # Set default provider
        self.default_provider = settings.default_model
        if self.default_provider not in self.providers:
            # Fallback to first available provider
            self.default_provider = list(self.providers.keys())[0] if self.providers else None
    
    async def get_response(self, prompt: str, provider: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Get response from specified or default provider."""
        provider_name = provider or self.default_provider
        
        if not provider_name or provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not available. Available: {list(self.providers.keys())}")
        
        return await self.providers[provider_name].generate_response(prompt, **kwargs)
    
    async def close(self) -> None:
        """Close all providers."""
        for provider in self.providers.values():
            await provider.close()
        self.providers.clear()
