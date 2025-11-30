"""
Game Model

Represents the state of an Oh Hell! game.
"""

from datetime import datetime


class Game:
    """
    Game state model to track the entire game.
    
    Attributes:
        tournament_name (str): Name of the tournament (Google Sheet file)
        tournament_id (str): Google Sheet ID
        players (list): List of Player objects in play order
        game_mode (str): Game direction mode
        hands (list): List of hand configurations
        current_hand_index (int): Index of current hand being played
        dealer_index (int): Index of current dealer
        sheet_name (str): Name of game sheet in Google Sheets
    """
    
    def __init__(self, tournament_name, tournament_id, players, game_mode, hands):
        """
        Initialize a game.
        
        Args:
            tournament_name (str): Tournament name
            tournament_id (str): Google Sheet ID
            players (list): List of Player objects
            game_mode (str): 'up', 'down', 'up_then_down', 'down_then_up'
            hands (list): List of hand dicts with {cards, dealer_index}
        """
        self.tournament_name = tournament_name
        self.tournament_id = tournament_id
        self.players = players
        self.game_mode = game_mode
        self.hands = hands
        self.current_hand_index = 0
        self.dealer_index = hands[0]['dealer_index'] if hands else 0
        
        # Generate sheet name with timestamp
        now = datetime.now()
        self.sheet_name = now.strftime('%y-%m-%d#%H-%M-%S')
        
        # Current hand state
        self.current_bids = {}  # {player_name: bid}
        self.current_tricks = {}  # {player_name: tricks_won}
    
    def get_current_hand(self):
        """
        Get current hand configuration.
        
        Returns:
            dict: Hand configuration or None if game complete
        """
        if self.current_hand_index < len(self.hands):
            return self.hands[self.current_hand_index]
        return None
    
    def get_current_dealer(self):
        """
        Get current dealer player.
        
        Returns:
            Player: Current dealer
        """
        return self.players[self.dealer_index]
    
    def advance_to_next_hand(self):
        """Advance to the next hand and update dealer."""
        self.current_hand_index += 1
        self.current_bids = {}
        self.current_tricks = {}
        
        if self.current_hand_index < len(self.hands):
            # Update dealer to next hand's dealer
            self.dealer_index = self.hands[self.current_hand_index]['dealer_index']
    
    def is_complete(self):
        """
        Check if game is finished.
        
        Returns:
            bool: True if all hands played
        """
        return self.current_hand_index >= len(self.hands)
    
    def to_dict(self):
        """
        Convert game to dictionary representation.
        
        Returns:
            dict: Game data
        """
        return {
            'tournament_name': self.tournament_name,
            'tournament_id': self.tournament_id,
            'players': [p.to_dict() for p in self.players],
            'game_mode': self.game_mode,
            'hands': self.hands,
            'current_hand_index': self.current_hand_index,
            'dealer_index': self.dealer_index,
            'sheet_name': self.sheet_name,
            'current_bids': self.current_bids,
            'current_tricks': self.current_tricks
        }
    
    @staticmethod
    def from_dict(data):
        """
        Create a Game instance from dictionary data.
        
        Args:
            data (dict): Dictionary with game data
            
        Returns:
            Game: New Game instance
        """
        from app.models.player import Player
        
        players = [Player.from_dict(p) for p in data['players']]
        game = Game(
            tournament_name=data['tournament_name'],
            tournament_id=data['tournament_id'],
            players=players,
            game_mode=data['game_mode'],
            hands=data['hands']
        )
        game.current_hand_index = data.get('current_hand_index', 0)
        game.dealer_index = data.get('dealer_index', 0)
        game.sheet_name = data.get('sheet_name', game.sheet_name)
        game.current_bids = data.get('current_bids', {})
        game.current_tricks = data.get('current_tricks', {})
        
        return game
