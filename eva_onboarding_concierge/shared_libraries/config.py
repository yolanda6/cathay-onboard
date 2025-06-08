"""
Central Configuration for Eva Onboarding Concierge
Manages all project settings, environment variables, and shared configurations.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EvaConfig:
    """Central configuration class for all Eva agents."""
    
    # Google Cloud Configuration
    PROJECT_ID: str = os.getenv("GOOGLE_CLOUD_PROJECT", "vital-octagon-19612")
    LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    STAGING_BUCKET: str = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "gs://2025-cathay-agentspace")
    
    # Model Configuration
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    
    # Environment Variables
    GOOGLE_GENAI_USE_VERTEXAI: str = "TRUE"
    
    @classmethod
    def setup_environment(cls) -> None:
        """Set up environment variables for all agents."""
        os.environ["GOOGLE_CLOUD_PROJECT"] = cls.PROJECT_ID
        os.environ["GOOGLE_CLOUD_LOCATION"] = cls.LOCATION
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = cls.GOOGLE_GENAI_USE_VERTEXAI
    
    @classmethod
    def get_project_config(cls) -> dict:
        """Get project configuration as dictionary."""
        return {
            "project_id": cls.PROJECT_ID,
            "location": cls.LOCATION,
            "staging_bucket": cls.STAGING_BUCKET,
            "model": cls.GEMINI_MODEL
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present."""
        required_vars = [cls.PROJECT_ID, cls.LOCATION, cls.STAGING_BUCKET]
        return all(var for var in required_vars)
    
    @classmethod
    def print_config(cls) -> None:
        """Print current configuration for debugging."""
        print("🔧 Eva Onboarding Concierge Configuration")
        print("=" * 50)
        print(f"📋 PROJECT_ID: {cls.PROJECT_ID}")
        print(f"📍 LOCATION: {cls.LOCATION}")
        print(f"📦 STAGING_BUCKET: {cls.STAGING_BUCKET}")
        print(f"🤖 MODEL: {cls.GEMINI_MODEL}")
        print(f"✅ Valid Config: {cls.validate_config()}")
        print()

# Initialize environment on import
EvaConfig.setup_environment()

# Export configuration instance
config = EvaConfig()

# Convenience exports
PROJECT_ID = EvaConfig.PROJECT_ID
LOCATION = EvaConfig.LOCATION
STAGING_BUCKET = EvaConfig.STAGING_BUCKET
GEMINI_MODEL = EvaConfig.GEMINI_MODEL

__all__ = [
    'EvaConfig',
    'config', 
    'PROJECT_ID',
    'LOCATION', 
    'STAGING_BUCKET',
    'GEMINI_MODEL'
]
