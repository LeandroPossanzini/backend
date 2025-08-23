import threading
from system.analytics_repository import save_analytics
from system.articles_repository import get_first_matching_articles

MAX_RESULTS = 5

def process_search(title, username):
    """
    Lógica de búsqueda de artículos (hasta MAX_RESULTS) y registro de analítica.
    """
    # Obtener artículos de manera eficiente
    articles = get_first_matching_articles(title, MAX_RESULTS)

    # Guardar analítica en segundo plano
    threading.Thread(target=save_analytics, args=(username, title)).start()

    return articles
