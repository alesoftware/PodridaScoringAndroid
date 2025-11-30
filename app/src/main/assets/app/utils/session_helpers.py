from flask import session

def clear_game_session(keep_config=False):
    """
    Clear game-related data from the session.
    
    Args:
        keep_config (bool): If True, keeps configuration data (players, mode, hands, order)
                           and only clears the active game state.
    """
    # Always clear the active game state
    session.pop('game', None)
    
    if not keep_config:
        # Clear configuration data
        session.pop('selected_players', None)
        session.pop('game_mode', None)
        session.pop('selected_hands', None)
        session.pop('player_order', None)
        session.pop('first_dealer_index', None)
        session.pop('single_card_dealers', None)
