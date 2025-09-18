"""Test data models."""

import pytest
from src.portfolio.models.chat import ChatMessage, ChatResponse, ModelProvider
from src.portfolio.models.resources import Resource, ResourceType, ResourcesConfig


def test_chat_message_validation():
    """Test ChatMessage model validation."""
    # Valid message
    message = ChatMessage(message="Hello, how are you?")
    assert message.message == "Hello, how are you?"
    assert message.model_provider is None
    
    # With model provider
    message_with_provider = ChatMessage(
        message="Hello", 
        model_provider=ModelProvider.TOGETHER
    )
    assert message_with_provider.model_provider == ModelProvider.TOGETHER


def test_chat_response_creation():
    """Test ChatResponse model creation."""
    response = ChatResponse(
        response="I'm doing well, thank you!",
        confidence=0.95,
        model_used="together",
        processing_time=1.2
    )
    assert response.response == "I'm doing well, thank you!"
    assert response.confidence == 0.95
    assert response.model_used == "together"
    assert response.processing_time == 1.2


def test_resource_creation():
    """Test Resource model creation."""
    resource = Resource(
        name="LinkedIn Profile",
        url="https://linkedin.com/in/test",
        type=ResourceType.SOCIAL,
        description="Professional LinkedIn profile"
    )
    assert resource.name == "LinkedIn Profile"
    assert resource.type == ResourceType.SOCIAL
    assert resource.url == "https://linkedin.com/in/test"


def test_resources_config():
    """Test ResourcesConfig model."""
    config = ResourcesConfig()
    assert config.profiles == {}
    assert config.projects == {}
    assert config.additional == {}
    assert config.resume is None
