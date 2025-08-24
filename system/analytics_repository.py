import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS_FILE = os.path.join(BASE_DIR, "db", "analytics.txt")

def get_last_search_system(username: str) -> str | None:
    if not os.path.exists(ANALYTICS_FILE):
        logging.warning("Archivo de analytics no encontrado.")
        return None
    try:
        with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines):
            if line.startswith(username + " searched:"):
                return line.split("searched:")[1].strip()
        logging.info(f"No se encontró búsqueda para usuario: {username}")
        return None
    except Exception as e:
        logging.error(f"Error leyendo analytics: {e}")
        return None

def save_analytics_system(username: str, search_word: str):
    if not username:
        username = "desconocido"
    os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
    try:
        with open(ANALYTICS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{username} searched: {search_word}\n")
        logging.info(f"Analytics guardado para usuario: {username}, búsqueda: {search_word}")
    except Exception as e:
        logging.error(f"Error guardando analytics: {e}")