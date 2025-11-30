import gspread
from google.oauth2.service_account import Credentials
from app.config import Config

class BaseSheetsService:
    """Base service for Google Sheets operations."""
    
    def __init__(self):
        """Initialize Google Sheets service with service account credentials."""
        # Define the required scopes
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        try:
            # Load credentials from service account file
            creds = Credentials.from_service_account_file(
                Config.GOOGLE_SERVICE_ACCOUNT_FILE,
                scopes=scopes
            )
            self.client = gspread.authorize(creds)
        except Exception as e:
            print(f"Warning: Could not initialize Google Sheets: {e}")
            self.client = None

    def get_spreadsheet(self, sheet_id):
        """
        Get a spreadsheet by ID.
        
        Args:
            sheet_id (str): Google Sheet ID
            
        Returns:
            Spreadsheet: Spreadsheet object or None
        """
        if not self.client:
            return None
        
        try:
            return self.client.open_by_key(sheet_id)
        except Exception as e:
            print(f"Error opening spreadsheet: {e}")
            return None

    @staticmethod
    def _column_letter(col_num):
        """
        Convert column number to letter (1=A, 2=B, etc.).
        
        Args:
            col_num (int): Column number (1-indexed)
            
        Returns:
            str: Column letter
        """
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + 65) + result
            col_num //= 26
        return result
