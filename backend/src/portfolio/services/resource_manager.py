"""Resource management service for handling portfolio resources."""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from src.portfolio.models.resources import ResourcesConfig, Resource, ResourceType
from config.settings import settings


class ResourceManager:
    """Manages portfolio resources and their configuration."""
    
    def __init__(self):
        self.resources_config: Optional[ResourcesConfig] = None
        self.resources_dir = Path(settings.resources_dir)
        self.config_file = self.resources_dir / settings.resources_config_file
    
    async def load_resources(self) -> ResourcesConfig:
        """Load resources configuration from YAML file."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Resources config file not found: {self.config_file}")
        
        with open(self.config_file, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
        
        # Parse the configuration
        self.resources_config = self._parse_config(config_data)
        return self.resources_config
    
    def _parse_config(self, config_data: Dict[str, Any]) -> ResourcesConfig:
        """Parse YAML configuration into ResourcesConfig model."""
        resources_config = ResourcesConfig()
        
        # Parse resume
        if "resume" in config_data.get("resources", {}):
            resume_data = config_data["resources"]["resume"]
            resources_config.resume = Resource(
                name="Resume",
                path=resume_data.get("path"),
                type=ResourceType(resume_data.get("type", "pdf")),
                description=resume_data.get("description", "Professional resume")
            )
        
        # Parse profiles
        profiles_data = config_data.get("resources", {}).get("profiles", {})
        for profile_name, profile_data in profiles_data.items():
            resources_config.profiles[profile_name] = Resource(
                name=profile_name.title(),
                url=profile_data.get("url"),
                type=ResourceType(profile_data.get("type", "social")),
                description=profile_data.get("description", f"{profile_name} profile")
            )
        
        # Parse projects
        projects_data = config_data.get("resources", {}).get("projects", {})
        for project_name, project_data in projects_data.items():
            if isinstance(project_data, list):
                # Multiple resources for a project
                project_resources = []
                for item in project_data:
                    project_resources.append(Resource(
                        name=item.get("name", project_name),
                        url=item.get("url"),
                        type=ResourceType(item.get("type", "project")),
                        description=item.get("description", f"{project_name} resource")
                    ))
                resources_config.projects[project_name] = project_resources
            else:
                # Single resource for a project
                resources_config.projects[project_name] = [Resource(
                    name=project_name.title(),
                    url=project_data.get("url"),
                    type=ResourceType(project_data.get("type", "project")),
                    description=project_data.get("description", f"{project_name} project")
                )]
        
        # Parse additional resources
        resources_config.additional = config_data.get("resources", {}).get("additional", {})
        
        return resources_config
    
    def get_resume_path(self) -> Optional[Path]:
        """Get the path to the resume PDF file."""
        if not self.resources_config or not self.resources_config.resume:
            return None
        
        resume_path = self.resources_dir / self.resources_config.resume.path
        return resume_path if resume_path.exists() else None
    
    def get_profile_urls(self) -> Dict[str, str]:
        """Get all profile URLs."""
        if not self.resources_config:
            return {}
        
        return {
            name: resource.url 
            for name, resource in self.resources_config.profiles.items() 
            if resource.url
        }
    
    def get_project_urls(self) -> Dict[str, List[str]]:
        """Get all project URLs."""
        if not self.resources_config:
            return {}
        
        project_urls = {}
        for project_name, resources in self.resources_config.projects.items():
            urls = [resource.url for resource in resources if resource.url]
            if urls:
                project_urls[project_name] = urls
        
        return project_urls
    
    def get_all_urls(self) -> List[str]:
        """Get all URLs from all resources."""
        urls = []
        
        # Add profile URLs
        urls.extend(self.get_profile_urls().values())
        
        # Add project URLs
        for project_urls in self.get_project_urls().values():
            urls.extend(project_urls)
        
        return urls
    
    def get_resource_summary(self) -> str:
        """Get a text summary of all resources."""
        if not self.resources_config:
            return "No resources configured."
        
        summary_parts = []
        
        # Add resume info
        if self.resources_config.resume:
            summary_parts.append(f"Resume: {self.resources_config.resume.description}")
        
        # Add profiles
        if self.resources_config.profiles:
            profile_names = list(self.resources_config.profiles.keys())
            summary_parts.append(f"Profiles: {', '.join(profile_names)}")
        
        # Add projects
        if self.resources_config.projects:
            project_names = list(self.resources_config.projects.keys())
            summary_parts.append(f"Projects: {', '.join(project_names)}")
        
        return " | ".join(summary_parts)
