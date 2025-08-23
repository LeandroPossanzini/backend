import json

ARTICLES_FILE = "db/articles.json"
MAX_RESULTS = 5

def get_first_matching_articles(title, max_results=MAX_RESULTS):
    results = []
    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except FileNotFoundError:
        return []

    # Buscar coincidencias parciales
    results = [
        a for a in articles if title.lower() in a.get("title", "").lower()
    ][:max_results]

    # Si no encontró ninguno, tomar los primeros max_results artículos
    if not results:
        results = articles[:max_results]

    return results
