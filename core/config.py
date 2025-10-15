"""
Configuration management for the application.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Settings:
    """Application settings."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize settings.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        # Database settings
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./getmeoutofhere.db")
        
        # App settings
        self.app_title = "GetMeOutOfHere"
        self.app_description = "Automated Job Application System"
        self.app_version = "2.0.0"
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_path):
            return self._get_default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f) or self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'score_threshold': 8.5,
            'job_search': {
                'keywords': [],
                'locations': [],
                'job_boards': []
            },
            'preferences': {
                'min_salary': 0,
                'target_salary': 0,
                'required_skills': [],
                'experience_level': 'mid'
            },
            'application': {
                'auto_apply': False,
                'dry_run': True,
                'max_applications_per_day': 10
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def get_score_threshold(self) -> float:
        """Get score threshold."""
        return self.config.get('score_threshold', 8.5)
    
    def get_scoring_weights(self) -> Dict[str, float]:
        """Get scoring weights."""
        return self.config.get('scoring_weights', {})
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return self.config.get('preferences', {})


# Global settings instance
settings = Settings()
