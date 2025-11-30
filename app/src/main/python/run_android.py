"""
Punto de entrada para la app Android.
Flask corre en modo local sin reload.
"""
import os
import sys

# Debug: Mostrar rutas de Python
print("=== PYTHON PATH DEBUG ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print("Python path:")
for path in sys.path:
    print(f"  - {path}")
print("=== END DEBUG ===")

# Configuración para Android
os.environ['DEV_MODE'] = 'False'
os.environ['FLASK_ENV'] = 'production'

# Configurar entorno Android
try:
    from android_config import setup_android_env
    setup_android_env()
except Exception as e:
    print(f"Warning: Could not load android_config: {e}")

# Importar la app Flask
try:
    from app import create_app
except ImportError as e:
    print(f"ERROR importing app: {e}")
    print("Trying to add current directory to path...")
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    print(f"Added {current_dir} to sys.path")
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
