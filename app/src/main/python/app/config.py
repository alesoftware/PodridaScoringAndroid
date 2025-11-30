"""
Oh Hell! Card Game Scorer - Configuration Management

This module manages application configuration from environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Development Mode
    DEV_MODE = os.getenv('DEV_MODE', 'False').lower() == 'true'
    
    # Admin Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
    
    # Google Sheets API
    GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'credentials.json')
    USERS_SHEET_ID = os.getenv('USERS_SHEET_ID', '')
    
    @staticmethod
    def is_development():
        """Check if running in development mode."""
        return Config.DEV_MODE
    
    @staticmethod
    def validate_config():
        """
        Validate required configuration values.
        
        Raises:
            ValueError: If required configuration is missing
        """
        if not Config.is_development():
            if not os.path.exists(Config.GOOGLE_SERVICE_ACCOUNT_FILE):
                raise ValueError(f"Google service account file not found: {Config.GOOGLE_SERVICE_ACCOUNT_FILE}")
            
            if not Config.USERS_SHEET_ID:
                raise ValueError("USERS_SHEET_ID environment variable is required in production")
            
            if Config.SECRET_KEY == 'dev-secret-key-change-me':
                raise ValueError("SECRET_KEY must be changed in production")
