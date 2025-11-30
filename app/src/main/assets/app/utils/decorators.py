from functools import wraps
from flask import session, flash, redirect, url_for, jsonify, request

def require_players(f):
    """Decorator to require selected players in session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('selected_players'):
            flash('Please select players first', 'error')
            return redirect(url_for('tournament.select_players'))
        return f(*args, **kwargs)
    return decorated_function

def require_game_config(f):
    """Decorator to require full game configuration (players and hands) in session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for players
        if not session.get('selected_players') and not session.get('player_order'):
            # player_order is set in /order/save, so if we are past that, selected_players might be irrelevant if we only use player_order?
            # But the flow usually keeps selected_players.
            # Let's stick to the logic found in the routes:
            # /order checks selected_players and selected_hands
            # /dealer checks player_order and selected_hands
            pass

        # Logic from /order
        if not session.get('selected_players') or not session.get('selected_hands'):
            flash('Please complete previous configuration steps', 'error')
            return redirect(url_for('tournament.select_players'))
        return f(*args, **kwargs)
    return decorated_function

def require_dealer_config(f):
    """Decorator to require player order and hands for dealer configuration."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Logic from /dealer
        if not session.get('player_order') or not session.get('selected_hands'):
            flash('Please complete previous configuration steps', 'error')
            return redirect(url_for('tournament.select_players'))
        return f(*args, **kwargs)
    return decorated_function

def require_active_game(f):
    """Decorator to require an active game in session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('game'):
            if request.is_json or request.path.endswith('/bid') or request.path.endswith('/tricks'):
                return jsonify({'success': False, 'error': 'No active game'})
            flash('No active game', 'error')
            return redirect(url_for('tournament.select_tournament'))
        return f(*args, **kwargs)
    return decorated_function
