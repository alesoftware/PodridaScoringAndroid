"""
Authentication Routes

Handles login, logout, and authentication flow.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import AuthService
from app.config import Config

bp = Blueprint('auth', __name__)


@bp.route('/')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication handler."""
    # Check if already logged in
    if 'username' in session:
        return redirect(url_for('tournament.select_tournament'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Attempt authentication
        user = AuthService.authenticate_user(username, password)
        
        if user:
            session['username'] = user.username
            session['is_admin'] = AuthService.is_admin(user.username)
            flash('Login successful!', 'success')
            
            # Redirect admin to user management, others to tournament selection
            if session['is_admin']:
                return redirect(url_for('admin.manage_users'))
            else:
                return redirect(url_for('tournament.select_tournament'))
        else:
            flash('Invalid username or password', 'error')
    
    # Show bypass button in development mode
    dev_mode = Config.is_development()
    print(f"DEBUG: dev_mode = {dev_mode}, Config.DEV_MODE = {Config.DEV_MODE}")
    
    return render_template('login.html', dev_mode=dev_mode)


@bp.route('/debug')
def debug_config():
    """Debug endpoint to check configuration."""
    from app.config import Config
    return f"""
    <pre>
    DEV_MODE: {Config.DEV_MODE}
    is_development(): {Config.is_development()}
    ADMIN_USERNAME: {Config.ADMIN_USERNAME}
    ADMIN_PASSWORD: {Config.ADMIN_PASSWORD}
    </pre>
    """


@bp.route('/dev-bypass')
def dev_bypass():
    """Development mode bypass (only works in dev mode)."""
    if not AuthService.can_bypass_auth():
        flash('Development bypass is not enabled', 'error')
        return redirect(url_for('auth.login'))
    
    # Log in as dev user
    session['username'] = 'dev_user'
    session['is_admin'] = False
    flash('Bypassed authentication (DEV MODE)', 'warning')
    
    return redirect(url_for('tournament.select_tournament'))


@bp.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


def login_required(f):
    """Decorator to require login for routes."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """Decorator to require admin access for routes."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        
        if not session.get('is_admin', False):
            flash('Admin access required', 'error')
            return redirect(url_for('tournament.select_tournament'))
        
        return f(*args, **kwargs)
    
    return decorated_function
