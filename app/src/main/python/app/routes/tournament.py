"""
Tournament Routes

Handles tournament selection and player management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.routes.auth import login_required
from app.services.tournament_service import TournamentService
from app.config import Config

bp = Blueprint('tournament', __name__, url_prefix='/tournament')


@bp.route('/')
@login_required
def select_tournament():
    """Tournament selection page."""
    tournament_service = TournamentService()
    all_spreadsheets = tournament_service.list_spreadsheets()
    
    # Filter out the Users sheet and Tournament Template
    spreadsheets = [
        sheet for sheet in all_spreadsheets 
        if sheet['id'] != Config.USERS_SHEET_ID and sheet['name'] != 'Tournament Template'
    ]
    
    return render_template('tournament.html', spreadsheets=spreadsheets)


@bp.route('/select', methods=['POST'])
@login_required
def set_tournament():
    """Set the selected tournament."""
    tournament_id = request.form.get('tournament_id', '').strip()
    tournament_name = request.form.get('tournament_name', '').strip()
    
    if not tournament_id:
        flash('Please select a tournament', 'error')
        return redirect(url_for('tournament.select_tournament'))
    
    # Store in session
    session['tournament_id'] = tournament_id
    session['tournament_name'] = tournament_name
    
    flash(f'Tournament "{tournament_name}" selected', 'success')
    return redirect(url_for('tournament.select_players'))


@bp.route('/players')
@login_required
def select_players():
    """Player selection page."""
    tournament_id = session.get('tournament_id')
    
    if not tournament_id:
        flash('Please select a tournament first', 'error')
        return redirect(url_for('tournament.select_tournament'))
    
    tournament_service = TournamentService()
    players = tournament_service.get_all_players(tournament_id)
    
    # Get selected players from session
    selected_players = session.get('selected_players', [])
    
    return render_template('players.html', 
                         players=players, 
                         selected_players=selected_players,
                         tournament_name=session.get('tournament_name', ''))


@bp.route('/players/add', methods=['POST'])
@login_required
def add_player():
    """Add a new player to the tournament."""
    tournament_id = session.get('tournament_id')
    
    if not tournament_id:
        flash('Please select a tournament first', 'error')
        return redirect(url_for('tournament.select_tournament'))
    
    player_name = request.form.get('player_name', '').strip()
    
    if not player_name:
        flash('Player name is required', 'error')
        return redirect(url_for('tournament.select_players'))
    
    tournament_service = TournamentService()
    
    if tournament_service.add_player(tournament_id, player_name):
        flash(f'Player "{player_name}" added successfully', 'success')
    else:
        flash('Error adding player', 'error')
    
    return redirect(url_for('tournament.select_players'))


@bp.route('/players/select', methods=['POST'])
@login_required
def save_selected_players():
    """Save selected players to session."""
    selected_players = request.form.getlist('selected_players')
    
    if not selected_players:
        flash('Please select at least 2 players', 'error')
        return redirect(url_for('tournament.select_players'))
    
    if len(selected_players) < 2:
        flash('Please select at least 2 players', 'error')
        return redirect(url_for('tournament.select_players'))
    
    # Store in session
    session['selected_players'] = selected_players
    
    flash(f'{len(selected_players)} players selected', 'success')
    return redirect(url_for('game.configure_mode'))
