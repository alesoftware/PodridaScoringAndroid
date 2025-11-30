"""
Player Model

Represents a player in the Oh Hell! card game.
"""


class Player:
    """
    Player model for game participants.
    
    Attributes:
        name (str): Player's name
        total_score (int): Cumulative game score
        hands (list): List of hand results {bid, won, score}
        is_invicto (bool): True if player has exact bid in all hands
    """
    
    def __init__(self, name):
        """
        Initialize a player.
        
        Args:
            name (str): Player's name
        """
        self.name = name
        self.total_score = 0
        self.hands = []
        self.is_invicto = True
    
    def add_hand_result(self, bid, won, score):
        """
        Add a hand result and update total score.
        
        Args:
            bid (int): Number of tricks bid
            won (int): Number of tricks won
            score (int): Score for this hand
        """
        self.hands.append({
            'bid': bid,
            'won': won,
            'score': score
        })
        self.total_score += score
        
        # Update invicto status (exact bid = bid == won)
        if bid != won:
            self.is_invicto = False
    
    def to_dict(self):
        """
        Convert player to dictionary representation.
        
        Returns:
            dict: Player data
        """
        return {
            'name': self.name,
            'total_score': self.total_score,
            'hands': self.hands,
            'is_invicto': self.is_invicto
        }
    
    @staticmethod
    def from_dict(data):
        """
        Create a Player instance from dictionary data.
        
        Args:
            data (dict): Dictionary with player data
            
        Returns:
            Player: New Player instance
        """
        player = Player(data['name'])
        player.total_score = data.get('total_score', 0)
        player.hands = data.get('hands', [])
        player.is_invicto = data.get('is_invicto', True)
        return player
