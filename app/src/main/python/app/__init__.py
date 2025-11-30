"""
Oh Hell! Card Game Scorer - Flask Application Factory

This module initializes the Flask application using the application factory pattern.
"""

from flask import Flask
from dotenv import load_dotenv
import os

# Configurar entorno Android si está disponible
try:
    from android_config import setup_android_env, is_android
    if is_android():
        print("Detectado entorno Android")
        setup_android_env()
except ImportError:
    # No estamos en Android, usar configuración normal
    pass

# Load environment variables (solo si no es Android)
try:
    if not is_android():
        load_dotenv()
except:
    load_dotenv()


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    app.config['SESSION_COOKIE_HTTPONLY'] = os.getenv('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
    app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    
    # Register blueprints (routes)
    from app.routes import auth, admin, tournament, game
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(tournament.bp)
    app.register_blueprint(game.bp)
    
    return app
