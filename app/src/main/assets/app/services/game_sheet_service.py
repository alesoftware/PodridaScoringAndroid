import gspread
from app.sheet_config import SHEET_CONFIG
from app.services.base_sheets_service import BaseSheetsService

class GameSheetService(BaseSheetsService):
    """Service for Game Sheet management and scoring."""
    
    def create_game_sheet(self, tournament_id, sheet_name, tournament_name, players, game=None):
        """
        Create a new game sheet with proper table structure.
        
        Args:
            tournament_id (str): Tournament Google Sheet ID
            sheet_name (str): Name for the new sheet (YY-MM-DD#HH-MM-SS)
            tournament_name (str): Tournament name
            players (list): List of Player objects in play order
            game: Game object with hands information (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            sheet = self.get_spreadsheet(tournament_id)
            if not sheet:
                return False
            
            # Try to find and duplicate the Game Template worksheet
            worksheet = None
            try:
                template = sheet.worksheet('Game Template')
                worksheet = template.duplicate(new_sheet_name=sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                # If template doesn't exist, create new worksheet
                worksheet = sheet.add_worksheet(title=sheet_name, rows=200, cols=50)
            except Exception:
                # Fallback to creating new worksheet
                if worksheet is None:
                    worksheet = sheet.add_worksheet(title=sheet_name, rows=200, cols=50)
            
            # Build the header structure
            # Line 1: GAME [sheet name]
            worksheet.update('A1', f'GAME {sheet_name}')
            
            # Line 2: TOURNAMENT [file name]
            worksheet.update('A2', f'TOURNAMENT {tournament_name}')
            
            # Line 3: Number of hands
            num_hands = len(game.hands) if game else 0
            worksheet.update('A3', num_hands)
            worksheet.update('B3', 'number of hands')
            
            # Line 4: Total number of tricks
            total_tricks = sum(hand['cards'] for hand in game.hands) if game else 0
            worksheet.update('A4', total_tricks)
            worksheet.update('B4', 'total number of tricks')
            
            # Line 5: Blank
            
            # Line 6: Player names (starting from column B, 3 columns wide each)
            player_headers = []
            for i, player in enumerate(players):
                col_start = chr(66 + i * 3)  # B, E, H, K, etc.
                player_headers.append([player.name, '', ''])
            
            # Merge cells for player names
            for i, player in enumerate(players):
                col_start_index = 2 + i * 3  # B=2, E=5, H=8, etc.
                col_start = self._column_letter(col_start_index)
                col_end = self._column_letter(col_start_index + 2)
                worksheet.merge_cells(f'{col_start}6:{col_end}6')
                worksheet.update(f'{col_start}6', player.name)
            
            # Line 7: Total Score (initially 0)
            total_scores = []
            for i in range(len(players)):
                col = self._column_letter(2 + i * 3)
                worksheet.merge_cells(f'{col}7:{self._column_letter(2 + i * 3 + 2)}7')
                worksheet.update(f'{col}7', 0)
            
            # Line 8: BID, WON, SCORE headers for each player
            headers_row = []
            for _ in players:
                headers_row.extend(['BID', 'WON', 'SCORE'])
            
            start_col = 'B'
            end_col = self._column_letter(1 + len(headers_row))
            worksheet.update(f'{start_col}8:{end_col}8', [headers_row])
            
            # Format the header (bold, centered)
            try:
                # 1. Game Title (A1)
                self._apply_format(worksheet, 'A1', SHEET_CONFIG['game_title'])
                
                # 2. Tournament Name (A2)
                self._apply_format(worksheet, 'A2', SHEET_CONFIG['tournament_name'])
                
                # 3. Player Names (Row 6)
                # Calculate range for player names
                last_col_idx = 2 + (len(players) * 3) - 1 # B is 2
                last_col_letter = self._column_letter(last_col_idx)
                self._apply_format(worksheet, f'B6:{last_col_letter}6', SHEET_CONFIG['player_names'])
                
                # 4. Total Scores (Row 7)
                self._apply_format(worksheet, f'B7:{last_col_letter}7', SHEET_CONFIG['total_scores'])
                
                # 5. Headers (Row 8)
                self._apply_format(worksheet, f'B8:{last_col_letter}8', SHEET_CONFIG['headers'])
                
                # 6. Column Widths
                col_widths = SHEET_CONFIG['columns']
                requests = []
                
                # Column A (Hand #) - Index 0
                requests.append({
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": worksheet.id,
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 1
                        },
                        "properties": {
                            "pixelSize": col_widths['cards_dealt']['pixelSize']
                        },
                        "fields": "pixelSize"
                    }
                })
                
                # Player Columns
                for i in range(len(players)):
                    base_col_idx = 1 + (i * 3) # B is index 1 (0-based for API)
                    
                    # Bid Column
                    requests.append({
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": worksheet.id,
                                "dimension": "COLUMNS",
                                "startIndex": base_col_idx,
                                "endIndex": base_col_idx + 1
                            },
                            "properties": {
                                "pixelSize": col_widths['bid']['pixelSize']
                            },
                            "fields": "pixelSize"
                        }
                    })
                    
                    # Won Column
                    requests.append({
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": worksheet.id,
                                "dimension": "COLUMNS",
                                "startIndex": base_col_idx + 1,
                                "endIndex": base_col_idx + 2
                            },
                            "properties": {
                                "pixelSize": col_widths['won']['pixelSize']
                            },
                            "fields": "pixelSize"
                        }
                    })
                    
                    # Score Column
                    requests.append({
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": worksheet.id,
                                "dimension": "COLUMNS",
                                "startIndex": base_col_idx + 2,
                                "endIndex": base_col_idx + 3
                            },
                            "properties": {
                                "pixelSize": col_widths['score']['pixelSize']
                            },
                            "fields": "pixelSize"
                        }
                    })
                
                if requests:
                    worksheet.spreadsheet.batch_update({"requests": requests})
                    
            except Exception as e:
                print(f"Error applying formatting: {e}")
            
            return True
        except Exception as e:
            print(f"Error creating game sheet: {e}")
            return False

    def _apply_format(self, worksheet, range_name, format_dict):
        """
        Apply formatting to a range based on config dict.
        
        Args:
            worksheet: gspread worksheet object
            range_name (str): Cell range (e.g., 'A1' or 'A1:B2')
            format_dict (dict): Formatting configuration
        """
        try:
            worksheet.format(range_name, format_dict)
        except Exception as e:
            print(f"Error formatting range {range_name}: {e}")
    
    def add_hand_result(self, tournament_id, sheet_name, hand_number, players_data):
        """
        Add a hand result to the game sheet.
        
        Args:
            tournament_id (str): Tournament Google Sheet ID
            sheet_name (str): Game sheet name
            hand_number (int): Number of cards dealt this hand
            players_data (list): List of dicts with {bid, won, score} for each player
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            sheet = self.get_spreadsheet(tournament_id)
            if not sheet:
                return False
            
            worksheet = sheet.worksheet(sheet_name)
            
            # Find next empty row (starting from row 9)
            next_row = len(worksheet.col_values(1)) + 1
            if next_row < 9:
                next_row = 9
            
            # Build row data: [hand_number, bid1, won1, score1, bid2, won2, score2, ...]
            row_data = [hand_number]
            for player_data in players_data:
                row_data.extend([player_data['bid'], player_data['won'], player_data['score']])
            
            # Update the row
            end_col = self._column_letter(len(row_data))
            worksheet.update(f'A{next_row}:{end_col}{next_row}', [row_data])
            
            # Update total scores in row 5
            self._update_total_scores(worksheet, players_data)
            
            return True
        except Exception as e:
            print(f"Error adding hand result: {e}")
            return False
    
    def _update_total_scores(self, worksheet, players_data):
        """Update total scores in row 7."""
        try:
            for i, player_data in enumerate(players_data):
                col = self._column_letter(2 + i * 3)
                # Get current total
                current_total = worksheet.acell(f'{col}7').value or '0'
                new_total = int(current_total) + player_data['score']
                worksheet.update(f'{col}7', new_total)
        except Exception as e:
            print(f"Error updating total scores: {e}")
