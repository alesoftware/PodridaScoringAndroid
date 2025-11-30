"""
Configuración para la versión Android.
Las credenciales se almacenan en el dispositivo.
"""
import os

# Configuración por defecto para Android
ANDROID_CONFIG = {
    'SECRET_KEY': 'android-secret-key-change-in-production-12345678',
    'ADMIN_USERNAME': 'admin',
    'ADMIN_PASSWORD': 'admin',  # Usuario debe cambiar en primera ejecución
    'GOOGLE_SERVICE_ACCOUNT_FILE': 'credentials.json',
    'USERS_SHEET_ID': '',  # Usuario configura en primera ejecución
    'DEV_MODE': 'False',
    'FLASK_ENV': 'production',
    'SESSION_COOKIE_HTTPONLY': 'True',
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'SESSION_COOKIE_SECURE': 'False'
}

def setup_android_env():
    """Configura variables de entorno para Android."""
    print("=== CONFIGURANDO ENTORNO ANDROID ===")
    for key, value in ANDROID_CONFIG.items():
        if key not in os.environ or not os.environ[key]:
            os.environ[key] = value
            print(f"Configurado: {key}")
    print("=== CONFIGURACIÓN COMPLETADA ===")

def is_android():
    """Detecta si la app está corriendo en Android."""
    try:
        # Chaquopy proporciona el módulo 'android'
        import android
        return True
    except ImportError:
        return False

# Auto-configurar si estamos en Android
if is_android():
    setup_android_env()
