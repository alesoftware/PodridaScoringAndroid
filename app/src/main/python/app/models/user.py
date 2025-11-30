"""
User Model

Represents a user in the system with authentication capabilities.
"""

import bcrypt


class User:
    """
    User model with password hashing and validation.
    
    Attributes:
        username (str): Unique username
        password_hash (str): Bcrypt hashed password
    """
    
    def __init__(self, username, password_hash=None):
        """
        Initialize a user.
        
        Args:
            username (str): User's username
            password_hash (str, optional): Pre-hashed password. If not provided,
                                          use set_password() to hash a plain password.
        """
        self.username = username
        self.password_hash = password_hash
    
    def set_password(self, plain_password):
        """
        Hash and set the user's password.
        
        Args:
            plain_password (str): Plain text password to hash
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, plain_password):
        """
        Verify a password against the stored hash.
        
        Args:
            plain_password (str): Plain text password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        if not self.password_hash:
            return False
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self):
        """
        Convert user to dictionary representation.
        
        Returns:
            dict: User data (without password hash)
        """
        return {
            'username': self.username
        }
    
    @staticmethod
    def from_dict(data):
        """
        Create a User instance from dictionary data.
        
        Args:
            data (dict): Dictionary with 'username' and 'password_hash'
            
        Returns:
            User: New User instance
        """
        return User(
            username=data.get('username'),
            password_hash=data.get('password_hash')
        )
