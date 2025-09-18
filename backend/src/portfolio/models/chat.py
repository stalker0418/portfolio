"""Chat-related data models."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ModelProvider(str, Enum):
    """Supported AI model providers."""
    TOGETHER = "together"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class ChatMessage(BaseModel):
    """Chat message model."""
    message: str = Field(..., description="The user's message", min_length=1)
    model_provider: Optional[ModelProvider] = Field(default=None, description="Specific model provider to use")


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="The AI's response")
    confidence: Optional[float] = Field(default=None, description="Confidence score of the response")
    model_used: Optional[str] = Field(default=None, description="Model provider used for the response")
    processing_time: Optional[float] = Field(default=None, description="Time taken to process the request")


class PortfolioSummary(BaseModel):
    """Portfolio summary model."""
    summary: str = Field(..., description="Summary of the portfolio")
    last_updated: Optional[str] = Field(default=None, description="When the summary was last updated")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Status message")
    version: Optional[str] = Field(default=None, description="API version")
    uptime: Optional[float] = Field(default=None, description="Server uptime in seconds")
