"""Configuration management for Budget Buddy"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Application
    APP_NAME = os.getenv("APP_NAME", "Budget Buddy")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # AI Services
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Plaid (Optional)
    PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID", "")
    PLAID_SECRET = os.getenv("PLAID_SECRET", "")
    PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / "assets"
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if essential configuration is set"""
        return bool(cls.SUPABASE_URL and cls.SUPABASE_KEY)
    
    @classmethod
    def get_supabase_config(cls) -> dict:
        """Get Supabase configuration"""
        return {
            "url": cls.SUPABASE_URL,
            "key": cls.SUPABASE_KEY
        }
