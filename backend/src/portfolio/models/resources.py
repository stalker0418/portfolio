"""Resource-related data models."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ResourceType(str, Enum):
    """Types of resources."""
    PDF = "pdf"
    SOCIAL = "social"
    CONTENT = "content"
    PROJECT = "project"
    CERTIFICATION = "certification"


class Resource(BaseModel):
    """Individual resource model."""
    name: str = Field(..., description="Name of the resource")
    url: Optional[str] = Field(default=None, description="URL of the resource")
    path: Optional[str] = Field(default=None, description="Local file path")
    type: ResourceType = Field(..., description="Type of resource")
    description: str = Field(..., description="Description of the resource")


class ResourceGroup(BaseModel):
    """Group of related resources."""
    name: str = Field(..., description="Name of the resource group")
    resources: List[Resource] = Field(default_factory=list, description="List of resources in this group")


class ResourcesConfig(BaseModel):
    """Complete resources configuration."""
    resume: Optional[Resource] = Field(default=None, description="Resume resource")
    profiles: Dict[str, Resource] = Field(default_factory=dict, description="Profile resources")
    projects: Dict[str, List[Resource]] = Field(default_factory=dict, description="Project resources")
    additional: Dict[str, Any] = Field(default_factory=dict, description="Additional resources")
