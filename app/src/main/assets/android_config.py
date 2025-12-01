"""
Configuración para la versión Android.
Las credenciales se almacenan en el dispositivo.
"""
import os

# Configuración por defecto para Android
ANDROID_CONFIG = {
    'SECRET_KEY': 'b90c105023e538d213c768b0093421c3b3dde6bcbbe94416a685e3a94ae618ae',
    'ADMIN_USERNAME': 'admin',
    'ADMIN_PASSWORD': 'admin25007708@',  # Usuario debe cambiar en primera ejecución
    'GOOGLE_SERVICE_ACCOUNT_FILE': 'credentials.json',
    'USERS_SHEET_ID': '1VvPcAQ1KAYrM-sQuM1XAP7iYL9Uytvx6IALbA13-u1s',  # Usuario configura en primera ejecución
    'DEV_MODE': 'False',
    'FLASK_ENV': 'production',
    'SESSION_COOKIE_HTTPONLY': 'True',
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'SESSION_COOKIE_SECURE': 'False'
}

def setup_android_env():
    """Configura variables de entorno para Android."""
    print("=== CONFIGURANDO ENTORNO ANDROID ===")
    
    # En Android, buscar credentials.json en el directorio correcto
    import sys
    credentials_found = False
    
    # Debug: mostrar sys.path
    print("sys.path entries:")
    for path in sys.path:
        print(f"  - {path}")
        
    # Intentar encontrar credentials.json
    possible_paths = [
        'credentials.json',  # Relative to current directory
        '/data/data/com.alesoftware.podridascoring/files/chaquopy/AssetFinder/app/credentials.json',
    ]
    
    # Buscar en sys.path
    for base_path in sys.path:
        test_path = os.path.join(base_path, 'credentials.json')
        if os.path.exists(test_path):
            ANDROID_CONFIG['GOOGLE_SERVICE_ACCOUNT_FILE'] = test_path
            print(f"✓ Credentials found at: {test_path}")
            credentials_found = True
            break
    
    if not credentials_found:
        print("⚠ Warning: credentials.json not found in sys.path")
        # Intentar rutas posibles
        for test_path in possible_paths:
            if os.path.exists(test_path):
                ANDROID_CONFIG['GOOGLE_SERVICE_ACCOUNT_FILE'] = test_path
                print(f"✓ Credentials found at: {test_path}")
                credentials_found = True
                break
    
    if not credentials_found:
        print("✗ Could not find credentials.json")
    
    for key, value in ANDROID_CONFIG.items():
        if key not in os.environ or not os.environ[key]:
            os.environ[key] = value
            if key == 'GOOGLE_SERVICE_ACCOUNT_FILE':
                print(f"Configurado: {key} = {value}")
            elif key not in ['SECRET_KEY', 'ADMIN_PASSWORD']:
                print(f"Configurado: {key} = {value}")
            else:
                print(f"Configurado: {key} = ***")
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
