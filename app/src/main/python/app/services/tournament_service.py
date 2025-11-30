import gspread
from app.services.base_sheets_service import BaseSheetsService

class TournamentService(BaseSheetsService):
    """Service for Tournament and Player management."""
    
    def list_spreadsheets(self):
        """
        List all spreadsheets accessible to the service account.
        
        Returns:
            list: List of dicts with {id, name}
        """
        if not self.client:
            return []
        
        try:
            spreadsheets = self.client.openall()
            return [{'id': s.id, 'name': s.title} for s in spreadsheets]
        except Exception as e:
            print(f"Error listing spreadsheets: {e}")
            return []
    
    def create_tournament_sheet(self, tournament_name):
        """
        Create a new tournament Google Sheet with Players worksheet.
        
        Args:
            tournament_name (str): Name for the new tournament
            
        Returns:
            dict: {id, name} of created sheet or None if failed
        """
        if not self.client:
            return None
        
        try:
            # Create new spreadsheet
            spreadsheet = self.client.create(tournament_name)
            
            # Create Players worksheet
            try:
                # Rename the default sheet to "Players"
                sheet1 = spreadsheet.sheet1
                sheet1.update_title('Players')
                sheet1.update('A1', 'Player Name')
            except:
                # Or add Players worksheet if renaming fails
                worksheet = spreadsheet.add_worksheet(title='Players', rows=100, cols=1)
                worksheet.update('A1', 'Player Name')
            
            return {'id': spreadsheet.id, 'name': spreadsheet.title}
        except Exception as e:
            print(f"Error creating tournament sheet: {e}")
            return None
    
    def get_players_worksheet(self, sheet_id):
        """
        Get or create the Players worksheet in a tournament sheet.
        
        Args:
            sheet_id (str): Google Sheet ID
            
        Returns:
            Worksheet: Players worksheet or None
        """
        try:
            sheet = self.get_spreadsheet(sheet_id)
            if not sheet:
                return None
            
            try:
                return sheet.worksheet('Players')
            except gspread.exceptions.WorksheetNotFound:
                # Create the worksheet
                worksheet = sheet.add_worksheet(title='Players', rows=100, cols=1)
                worksheet.update('A1', 'Player Name')
                return worksheet
        except Exception as e:
            print(f"Error accessing Players worksheet: {e}")
            return None
    
    def get_all_players(self, sheet_id):
        """
        Get all players from a tournament sheet.
        
        Args:
            sheet_id (str): Google Sheet ID
            
        Returns:
            list: List of player names (sorted alphabetically)
        """
        worksheet = self.get_players_worksheet(sheet_id)
        if not worksheet:
            return []
        
        try:
            # Get all values from column A (skip header)
            values = worksheet.col_values(1)[1:]  # Skip header row
            # Filter out empty values and sort
            players = sorted([name for name in values if name.strip()])
            return players
        except Exception as e:
            print(f"Error getting players: {e}")
            return []
    
    def add_player(self, sheet_id, player_name):
        """
        Add a player to the Players worksheet.
        
        Args:
            sheet_id (str): Google Sheet ID
            player_name (str): Player name to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        worksheet = self.get_players_worksheet(sheet_id)
        if not worksheet:
            return False
        
        try:
            worksheet.append_row([player_name])
            return True
        except Exception as e:
            print(f"Error adding player: {e}")
            return False
