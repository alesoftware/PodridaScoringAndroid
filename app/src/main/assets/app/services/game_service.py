"""
Game Service

Handles game logic including scoring, hand generation, and Hook On rule.
"""


class GameService:
    """Service for game logic operations."""
    
    @staticmethod
    def calculate_max_cards(num_players):
        """
        Calculate maximum cards to deal based on number of players.
        Rule: Higher integer resulting from 52 / num_players
        
        Args:
            num_players (int): Number of players
            
        Returns:
            int: Maximum cards to deal
        """
        return 52 // num_players
    
    @staticmethod
    def generate_hands(num_players, mode):
        """
        Generate list of hands based on game mode.
        
        Args:
            num_players (int): Number of players
            mode (str): 'up', 'down', 'up_then_down', 'down_then_up'
            
        Returns:
            list: List of hand numbers (cards to deal)
        """
        max_cards = GameService.calculate_max_cards(num_players)
        
        if mode == 'up':
            # 1, 2, 3, ..., max_cards
            return list(range(1, max_cards + 1))
        elif mode == 'down':
            # max_cards, max_cards-1, ..., 1
            return list(range(max_cards, 0, -1))
        elif mode == 'up_then_down':
            # 1, 2, ..., max_cards, max_cards-1, ..., 1
            up = list(range(1, max_cards + 1))
            down = list(range(max_cards - 1, 0, -1))
            return up + down
        elif mode == 'down_then_up':
            # max_cards, max_cards-1, ..., 1, 2, ..., max_cards
            down = list(range(max_cards, 0, -1))
            up = list(range(2, max_cards + 1))
            return down + up
        else:
            return []
    
    @staticmethod
    def validate_dealer_bid(total_bids, dealer_bid, cards_dealt):
        """
        Check if dealer's bid violates Hook On rule.
        
        Args:
            total_bids (int): Sum of all other players' bids
            dealer_bid (int): Dealer's proposed bid
            cards_dealt (int): Number of cards dealt this hand
            
        Returns:
            bool: True if bid is valid, False if it violates Hook On
        """
        # Hook On rule: dealer cannot make total bids equal cards dealt
        return (total_bids + dealer_bid) != cards_dealt
    
    @staticmethod
    def calculate_hand_score(bid, won):
        """
        Calculate score for a hand.
        Scoring: 1 point per trick won, +10 bonus for exact bid
        
        Args:
            bid (int): Number of tricks bid
            won (int): Number of tricks won
            
        Returns:
            int: Score for the hand
        """
        score = won  # 1 point per trick won
        
        if bid == won:  # Exact bid
            score += 10
        
        return score
    
    @staticmethod
    def check_invicto_status(player):
        """
        Check if player has exact bid in all hands (INVICTO status).
        
        Args:
            player (Player): Player object with hands history
            
        Returns:
            bool: True if player made exact bid in all hands
        """
        if not player.hands:
            return True
        
        for hand in player.hands:
            if hand['bid'] != hand['won']:
                return False
        
        return True
    
    @staticmethod
    def get_sorted_players_by_score(players):
        """
        Sort players by total score (descending).
        
        Args:
            players (list): List of Player objects
            
        Returns:
            list: Sorted list of players
        """
        return sorted(players, key=lambda p: p.total_score, reverse=True)
    
    @staticmethod
    def calculate_next_dealer_index(current_dealer_index, num_players):
        """
        Calculate the next dealer's index (rotates clockwise).
        
        Args:
            current_dealer_index (int): Current dealer's index
            num_players (int): Total number of players
            
        Returns:
            int: Next dealer's index
        """
        return (current_dealer_index + 1) % num_players
    
    @staticmethod
    def get_bidding_order(dealer_index, num_players):
        """
        Get the order of players for bidding (starts after dealer, ends with dealer).
        
        Args:
            dealer_index (int): Dealer's index
            num_players (int): Total number of players
            
        Returns:
            list: List of player indices in bidding order
        """
        order = []
        for i in range(1, num_players + 1):
            order.append((dealer_index + i) % num_players)
        return order
