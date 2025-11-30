import gspread
from app.config import Config
from app.models.user import User
from app.services.base_sheets_service import BaseSheetsService

class UserService(BaseSheetsService):
    """Service for User management in Google Sheets."""
    
    def get_users_worksheet(self):
        """
        Get the users worksheet.
        
        Returns:
            Worksheet: Users worksheet or None
        """
        if not self.client or not Config.USERS_SHEET_ID:
            return None
        
        try:
            sheet = self.client.open_by_key(Config.USERS_SHEET_ID)
            return sheet.worksheet('users')
        except gspread.exceptions.WorksheetNotFound:
            # Create the worksheet if it doesn't exist
            sheet = self.client.open_by_key(Config.USERS_SHEET_ID)
            worksheet = sheet.add_worksheet(title='users', rows=100, cols=3)
            # Add headers
            worksheet.update('A1:B1', [['username', 'password_hash']])
            return worksheet
        except Exception as e:
            print(f"Error accessing users worksheet: {e}")
            return None
    
    def get_all_users(self):
        """
        Get all users from Google Sheets.
        
        Returns:
            list: List of User objects
        """
        worksheet = self.get_users_worksheet()
        if not worksheet:
            return []
        
        try:
            records = worksheet.get_all_records()
            users = []
            for record in records:
                if record.get('username'):  # Skip empty rows
                    user = User(
                        username=record['username'],
                        password_hash=record.get('password_hash', '')
                    )
                    users.append(user)
            return users
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_user_by_username(self, username):
        """
        Get a user by username.
        
        Args:
            username (str): Username to search for
            
        Returns:
            User: User object or None if not found
        """
        users = self.get_all_users()
        for user in users:
            if user.username == username:
                return user
        return None
    
    def add_user(self, user):
        """
        Add a new user to Google Sheets.
        
        Args:
            user (User): User object to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        worksheet = self.get_users_worksheet()
        if not worksheet:
            return False
        
        try:
            worksheet.append_row([user.username, user.password_hash])
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_user(self, old_username, updated_user):
        """
        Update an existing user.
        
        Args:
            old_username (str): Current username
            updated_user (User): Updated user object
            
        Returns:
            bool: True if successful, False otherwise
        """
        worksheet = self.get_users_worksheet()
        if not worksheet:
            return False
        
        try:
            # Find the user row
            cell = worksheet.find(old_username)
            if cell:
                row = cell.row
                worksheet.update(f'A{row}:B{row}', [[updated_user.username, updated_user.password_hash]])
                return True
            return False
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, username):
        """
        Delete a user from Google Sheets.
        
        Args:
            username (str): Username to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        worksheet = self.get_users_worksheet()
        if not worksheet:
            return False
        
        try:
            cell = worksheet.find(username)
            if cell:
                worksheet.delete_rows(cell.row)
                return True
            return False
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
