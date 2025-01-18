import json
import os

CONFIG_FILE = "config.json"

def save_config(theme_name):
    """Guarda la configuración del tema en un archivo JSON."""
    with open(CONFIG_FILE, "w") as config_file:
        json.dump({"theme": theme_name}, config_file)

def load_config():
    """Carga la configuración del tema desde un archivo JSON o crea uno nuevo."""
    if not os.path.exists(CONFIG_FILE):
        save_config("light")  # Crea el archivo con el tema por defecto
        print("Config no encontrado. La opción por defecto es 'light'.")
        return "light"

    try:
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            theme = config.get("theme", "light")
            return theme
    except json.JSONDecodeError:
        print("Error en el archivo de configuración. Usando tema predeterminado.")
        # Si el archivo es corrupto, devolvemos el tema predeterminado
        return "light"

