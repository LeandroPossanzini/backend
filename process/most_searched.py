import threading
import logging
from system.analytics_repository import save_analytics_system
from system.articles_repository import get_first_matching_articles

MAX_RESULTS = 5

def process_search(title, username):
    if not isinstance(title, str) or not title.strip():
        logging.warning("Título de búsqueda inválido.")
        return []

    if not isinstance(username, str) or not username.strip():
        username = "desconocido"

    articles = get_first_matching_articles(title, MAX_RESULTS)

    def save_analytics_safe():
        try:
            save_analytics_system(username, title)
        except Exception as e:
            logging.error(f"Error guardando analítica: {e}")

    threading.Thread(target=save_analytics_safe).start()

    logging.info(f"Búsqueda realizada: '{title}' por usuario: '{username}'")
    return articles