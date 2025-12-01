"""
Authentication Service

Handles user authentication and session management.
"""

from app.models.user import User
from app.config import Config
from app.services.user_service import UserService


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate a user with username and password.
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            User: Authenticated user object or None if authentication fails
        """
        # Check if admin credentials
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            admin_user = User(username)
            admin_user.set_password(Config.ADMIN_PASSWORD)
            return admin_user
        
        # Check regular users from Google Sheets
        try:
            user_service = UserService()
            user = user_service.get_user_by_username(username)
            
            if user and user.check_password(password):
                return user
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
        
        return None
    
    @staticmethod
    def is_admin(username):
        """
        Check if a user is the admin.
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if user is admin
        """
        return username == Config.ADMIN_USERNAME
    
    @staticmethod
    def can_bypass_auth():
        """
        Check if authentication can be bypassed (development mode).
        
        Returns:
            bool: True if in development mode and bypass is allowed
        """
        return Config.is_development()
