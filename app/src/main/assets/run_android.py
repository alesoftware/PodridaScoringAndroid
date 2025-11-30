"""
Punto de entrada para la app Android.
Flask corre en modo local sin reload.
"""
import os
import sys

# Configuración para Android
os.environ['DEV_MODE'] = 'False'
os.environ['FLASK_ENV'] = 'production'

# Importar la app Flask
from app import create_app

app = create_app()

def start_server():
    """Inicia el servidor Flask en modo Android."""
    print("=== INICIANDO FLASK DESDE ANDROID ===")
    print(f"Host: 127.0.0.1")
    print(f"Port: 5000")
    print(f"Python version: {sys.version}")
    
    try:
        app.run(
            host='127.0.0.1',  # Solo accesible localmente
            port=5000,
            debug=False,       # Sin debug en producción
            use_reloader=False # Sin auto-reload
        )
    except Exception as e:
        print(f"ERROR AL INICIAR FLASK: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    start_server()
