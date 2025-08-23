import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, "db", "articles.json")
FEATURED_FILE = os.path.join(BASE_DIR, "db", "featured_products.json")
MAX_RESULTS = 5


def get_first_matching_articles(title, max_results=MAX_RESULTS):
    results = []
    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except FileNotFoundError:
        return []

    results = [
        a for a in articles if title.lower() in a.get("title", "").lower()
    ][:max_results]

    if not results:
        results = articles[:max_results]

    return results


def load_json(file_path: str) -> list:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(file_path: str, data: list):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def update_article_system(article_id: str, new_data: dict):
    articles = load_json(ARTICLES_FILE)
    updated = False
    for article in articles:
        if str(article.get("id")) == str(article_id):
            article.update(new_data)
            updated = True
            break
    if updated:
        save_json(ARTICLES_FILE, articles)
    return updated

def delete_article_system(article_id: str) -> bool:
    articles = load_json(ARTICLES_FILE)
    new_articles = [a for a in articles if str(a.get("id")) != str(article_id)]

    if len(new_articles) == len(articles):
        return False  # no existía ese id

    save_json(ARTICLES_FILE, new_articles)
    return True

def create_article_system(new_data: dict) -> dict:
    articles = load_json(ARTICLES_FILE)

    # Buscar el último id existente (ejemplo: MLA100001)
    if articles:
        existing_ids = [a.get("id", "") for a in articles if isinstance(a.get("id"), str) and a.get("id", "").startswith("MLA")]
        if existing_ids:
            # Tomar el número más alto después de 'MLA'
            last_num = max([int(e.replace("MLA", "")) for e in existing_ids])
            new_id = f"MLA{last_num + 1:06d}"
        else:
            new_id = "MLA100001"
    else:
        new_id = "MLA100001"

    new_article = {"id": new_id, **new_data}
    articles.append(new_article)

    save_json(ARTICLES_FILE, articles)
    return new_article