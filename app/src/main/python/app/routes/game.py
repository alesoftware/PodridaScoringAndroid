"""
Game Routes

Handles game configuration, bidding, tricks, and scoring.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import json
from app.routes.auth import login_required
from app.services.game_service import GameService
from app.services.game_sheet_service import GameSheetService
from app.models.game import Game
from app.models.player import Player
from app.utils.decorators import require_players, require_game_config, require_dealer_config, require_active_game
from app.utils.session_helpers import clear_game_session

bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/mode')
@login_required
@require_players
def configure_mode():
    """Game mode configuration page."""
    selected_players = session.get('selected_players', [])
    
    # Generate available hands based on number of players
    max_cards = GameService.calculate_max_cards(len(selected_players))
    
    # Get current configuration from session
    game_mode = session.get('game_mode', 'down_then_up')
    
    # Initialize selected_hands if not in session
    if 'selected_hands' in session:
        selected_hands = session['selected_hands']
    else:
        # Generate default hands based on current game mode
        selected_hands = GameService.generate_hands(len(selected_players), game_mode)
    
    return render_template('game_mode.html',
                         max_cards=max_cards,
                         game_mode=game_mode,
                         selected_hands=selected_hands,
                         num_players=len(selected_players))


@bp.route('/mode/save', methods=['POST'])
@login_required
@require_players
def save_mode():
    """Save game mode configuration."""
    game_mode = request.form.get('game_mode', 'down_then_up')
    action = request.form.get('action', 'continue')
    
    # Store game mode in session
    session['game_mode'] = game_mode
    
    # Generate default hands based on mode (as a starting point)
    selected_players = session.get('selected_players', [])
    selected_hands = GameService.generate_hands(len(selected_players), game_mode)
    session['selected_hands'] = selected_hands
    
    if action == 'customize':
        return redirect(url_for('game.configure_hand_sequence'))
    else:
        flash('Game mode configured', 'success')
        return redirect(url_for('game.configure_order'))


@bp.route('/sequence')
@login_required
@require_players
def configure_hand_sequence():
    """Hand sequence customization page."""
    selected_players = session.get('selected_players', [])
        
    max_cards = GameService.calculate_max_cards(len(selected_players))
    selected_hands = session.get('selected_hands', [])
    
    return render_template('hand_sequence.html',
                         max_cards=max_cards,
                         selected_hands=selected_hands)


@bp.route('/sequence/save', methods=['POST'])
@login_required
def save_hand_sequence():
    """Save customized hand sequence."""
    hands_sequence_json = request.form.get('hands_sequence')
    selected_hands = []
    
    if hands_sequence_json:
        try:
            selected_hands = json.loads(hands_sequence_json)
            # Ensure all are integers
            selected_hands = [int(h) for h in selected_hands]
        except (ValueError, TypeError, json.JSONDecodeError):
            selected_hands = []
            
    if not selected_hands:
        flash('Please select at least one hand', 'error')
        return redirect(url_for('game.configure_hand_sequence'))
        
    session['selected_hands'] = selected_hands
    
    flash('Hand sequence saved', 'success')
    return redirect(url_for('game.configure_order'))


@bp.route('/order')
@login_required
@require_game_config
def configure_order():
    """Player order and dealer assignment page."""
    selected_players = session.get('selected_players', [])
    selected_hands = session.get('selected_hands', [])
    
    # Get current order from session or use alphabetical
    player_order = session.get('player_order', selected_players)
    first_dealer_index = session.get('first_dealer_index', 0)
    
    # Find single-card hands
    single_card_hands = [i for i, cards in enumerate(selected_hands) if cards == 1]
    single_card_dealers = session.get('single_card_dealers', {})
    
    return render_template('player_order.html',
                         players=player_order,
                         first_dealer_index=first_dealer_index,
                         selected_hands=selected_hands,
                         single_card_hands=single_card_hands,
                         single_card_dealers=single_card_dealers)


@bp.route('/order/save', methods=['POST'])
@login_required
def save_order():
    """Save player order."""
    player_order = request.form.getlist('player_order')
    
    # Store in session
    session['player_order'] = player_order
    
    flash('Player order configured', 'success')
    return redirect(url_for('game.configure_dealer'))


@bp.route('/dealer')
@login_required
@require_dealer_config
def configure_dealer():
    """Dealer assignment page."""
    selected_players = session.get('player_order', [])
    selected_hands = session.get('selected_hands', [])
    
    # Find single-card hands
    single_card_hands = [i for i, cards in enumerate(selected_hands) if cards == 1]
    
    return render_template('dealer_assignment.html',
                         players=selected_players,
                         single_card_hands=single_card_hands)


@bp.route('/dealer/save', methods=['POST'])
@login_required
@require_dealer_config
def save_dealer():
    """Save dealer assignment."""
    dealer_mode = request.form.get('dealer_mode', 'start')
    selected_dealer = int(request.form.get('selected_dealer', 0))
    player_order = session.get('player_order', [])
    
    num_players = len(player_order)
    first_dealer_index = 0
    
    if dealer_mode == 'start':
        first_dealer_index = selected_dealer
    else:
        # Single Card Hand Dealer
        # Find index of first 1-card hand
        selected_hands = session.get('selected_hands', [])
        try:
            first_single_card_index = selected_hands.index(1)
            # Calculate start dealer so that at first_single_card_index, the dealer is selected_dealer
            first_dealer_index = (selected_dealer - first_single_card_index) % num_players
        except ValueError:
            # No 1-card hand found, fallback to start dealer
            first_dealer_index = selected_dealer
    
    # Store in session
    session['first_dealer_index'] = first_dealer_index
    # Remove old single_card_dealers if present
    session.pop('single_card_dealers', None)
    
    flash('Dealer assignment configured', 'success')
    return redirect(url_for('game.summary'))


@bp.route('/summary')
@login_required
def summary():
    """Game summary page before starting."""
    # Get all configuration from session
    config = {
        'tournament_name': session.get('tournament_name', ''),
        'tournament_id': session.get('tournament_id', ''),
        'players': session.get('player_order', []),
        'game_mode': session.get('game_mode', ''),
        'selected_hands': session.get('selected_hands', []),
        'first_dealer_index': session.get('first_dealer_index', 0),
        'single_card_dealers': session.get('single_card_dealers', {})
    }
    
    return render_template('summary.html', config=config)


@bp.route('/start', methods=['POST'])
@login_required
def start_game():
    """Initialize game and create sheet."""
    # Get configuration from session
    tournament_id = session.get('tournament_id')
    tournament_name = session.get('tournament_name')
    player_names = session.get('player_order', [])
    game_mode = session.get('game_mode')
    selected_hands = session.get('selected_hands', [])
    first_dealer_index = session.get('first_dealer_index', 0)
    single_card_dealers = session.get('single_card_dealers', {})
    
    # Create Player objects
    players = [Player(name) for name in player_names]
    
    # Build hands configuration
    hands = []
    dealer_index = first_dealer_index
    
    for i, cards in enumerate(selected_hands):
        hands.append({
            'cards': cards,
            'dealer_index': dealer_index
        })
        
        # Rotate dealer for next hand
        dealer_index = GameService.calculate_next_dealer_index(dealer_index, len(players))
    
    # Create Game object
    game = Game(tournament_name, tournament_id, players, game_mode, hands)
    
    # Create game sheet in Google Sheets
    game_sheet_service = GameSheetService()
    if game_sheet_service.create_game_sheet(
        tournament_id,
        game.sheet_name,
        tournament_name,
        players,
        game
    ):
        # Store game in session
        session['game'] = game.to_dict()
        flash('Game started!', 'success')
        return redirect(url_for('game.play_hand'))
    else:
        flash('Error creating game sheet', 'error')
        return redirect(url_for('game.summary'))


@bp.route('/hand')
@login_required
@require_active_game
def play_hand():
    """Current hand bidding/playing page."""
    game_data = session.get('game')
    
    game = Game.from_dict(game_data)
    current_hand = game.get_current_hand()
    
    if not current_hand:
        flash('Game is complete!', 'success')
        return redirect(url_for('game.final_scores'))
    
    # Determine phase: bidding or playing
    num_players = len(game.players)
    bids_complete = len(game.current_bids) == num_players
    tricks_complete = len(game.current_tricks) == num_players
    
    # Get bidding order
    bidding_order = GameService.get_bidding_order(current_hand['dealer_index'], num_players)
    
    return render_template('bidding.html',
                         game=game,
                         current_hand=current_hand,
                         bids_complete=bids_complete,
                         tricks_complete=tricks_complete,
                         bidding_order=bidding_order)


# Additional game routes will be created in next batch
# (bid recording, tricks recording, scoring, etc.)


@bp.route('/hand/bid', methods=['POST'])
@login_required
@require_active_game
def record_bid():
    """Record a bid for a player."""
    game_data = session.get('game')
    
    game = Game.from_dict(game_data)
    current_hand = game.get_current_hand()
    
    player_name = request.form.get('player_name')
    bid = int(request.form.get('bid', 0))
    
    # Validate bid
    if bid < 0 or bid > current_hand['cards']:
        return jsonify({'success': False, 'error': 'Invalid bid'})
    
    # Check Hook On rule for dealer
    dealer = game.get_current_dealer()
    if player_name == dealer.name:
        total_other_bids = sum(game.current_bids.values())
        if not GameService.validate_dealer_bid(total_other_bids, bid, current_hand['cards']):
            return jsonify({'success': False, 'error': 'Hook On rule violation'})
    
    # Record bid
    game.current_bids[player_name] = bid
    
    # Update session
    session['game'] = game.to_dict()
    
    return jsonify({
        'success': True,
        'total_bids': sum(game.current_bids.values()),
        'bids_count': len(game.current_bids)
    })


@bp.route('/hand/tricks', methods=['POST'])
@login_required
@require_active_game
def record_tricks():
    """Record tricks won for a player."""
    game_data = session.get('game')
    
    game = Game.from_dict(game_data)
    current_hand = game.get_current_hand()
    
    player_name = request.form.get('player_name')
    tricks = int(request.form.get('tricks', 0))
    
    # Validate tricks
    if tricks < 0 or tricks > current_hand['cards']:
        return jsonify({'success': False, 'error': 'Invalid tricks count'})
    
    # Record tricks
    game.current_tricks[player_name] = tricks
    
    # Update session
    session['game'] = game.to_dict()
    
    return jsonify({'success': True})


@bp.route('/hand/calculate', methods=['POST'])
@login_required
@require_active_game
def calculate_scores():
    """Calculate scores for the current hand."""
    game_data = session.get('game')
    
    game = Game.from_dict(game_data)
    current_hand = game.get_current_hand()
    
    # Validate all tricks recorded
    if len(game.current_tricks) != len(game.players):
        flash('All tricks must be recorded', 'error')
        return redirect(url_for('game.play_hand'))
    
    # Calculate scores for each player
    players_data = []
    
    for player in game.players:
        bid = game.current_bids.get(player.name, 0)
        won = game.current_tricks.get(player.name, 0)
        score = GameService.calculate_hand_score(bid, won)
        
        # Update player
        player.add_hand_result(bid, won, score)
        
        players_data.append({
            'bid': bid,
            'won': won,
            'score': score
        })
    
    # Record in Google Sheets
    game_sheet_service = GameSheetService()
    game_sheet_service.add_hand_result(
        game.tournament_id,
        game.sheet_name,
        current_hand['cards'],
        players_data
    )
    
    # Advance to next hand
    game.advance_to_next_hand()
    
    # Update session
    session['game'] = game.to_dict()
    
    return redirect(url_for('game.show_scores', hand_cards=current_hand['cards']))


@bp.route('/scores/<int:hand_cards>')
@login_required
@require_active_game
def show_scores(hand_cards):
    """Show scores after a hand."""
    game_data = session.get('game')
    
    game = Game.from_dict(game_data)
    
    # Sort players by score
    sorted_players = GameService.get_sorted_players_by_score(game.players)
    
    # Check if game is complete
    is_complete = game.is_complete()
    
    # Get next hand info
    next_hand = game.get_current_hand() if not is_complete else None
    next_dealer = game.get_current_dealer() if not is_complete else None
    
    return render_template('scoring.html',
                         players=sorted_players,
                         hand_cards=hand_cards,
                         is_complete=is_complete,
                         next_hand=next_hand,
                         next_dealer=next_dealer,
                         game_mode=game.game_mode,
                         game=game)


@bp.route('/new-game', methods=['POST'])
@login_required
def new_game():
    """Start a completely new game."""
    # Clear game from session but keep tournament
    clear_game_session(keep_config=False)
    
    flash('Starting new game', 'success')
    return redirect(url_for('tournament.select_players'))


@bp.route('/new-game-same-config', methods=['POST'])
@login_required
def new_game_same_config():
    """Start new game with same configuration (skip to player order)."""
    # Clear only game data, keep configuration
    clear_game_session(keep_config=True)
    
    flash('Starting new game with same configuration', 'success')
    return redirect(url_for('game.configure_order'))


@bp.route('/final-scores')
@login_required
@require_active_game
def final_scores():
    """Show final scores (redirect to last hand scores)."""
    game_data = session.get('game')
    
    game = Game.from_dict(game_data)
    
    # Get the last hand that was played
    if game.current_hand_index > 0:
        last_hand = game.hands[game.current_hand_index - 1]
        return redirect(url_for('game.show_scores', hand_cards=last_hand['cards']))
    
    flash('No hands have been played', 'error')
    return redirect(url_for('tournament.select_tournament'))

