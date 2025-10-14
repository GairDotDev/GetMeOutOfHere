"""
Configuration loader for the job scraper application.
"""

import yaml
import os
from typing import Dict, Any


class ConfigLoader:
    """Loads and manages application configuration."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Dictionary containing configuration
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}. "
                f"Please create it from config.example.yaml"
            )
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate required fields
        self._validate_config(config)
        return config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate that required configuration fields are present.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ['score_threshold', 'scoring_weights', 'preferences', 'documents']
        missing_fields = [field for field in required_fields if field not in config]
        
        if missing_fields:
            raise ValueError(f"Missing required configuration fields: {missing_fields}")
        
        # Validate scoring weights sum to 1.0
        weights = config['scoring_weights']
        weight_sum = sum(weights.values())
        if not (0.99 <= weight_sum <= 1.01):  # Allow small floating point error
            raise ValueError(
                f"Scoring weights must sum to 1.0, got {weight_sum}. "
                f"Weights: {weights}"
            )
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (can use dot notation for nested keys)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_score_threshold(self) -> float:
        """Get the score threshold for auto-apply."""
        return self.config['score_threshold']
    
    def get_scoring_weights(self) -> Dict[str, float]:
        """Get the scoring weights."""
        return self.config['scoring_weights']
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return self.config['preferences']
    
    def get_documents_config(self) -> Dict[str, Any]:
        """Get documents configuration."""
        return self.config['documents']
