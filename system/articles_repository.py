import os
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, "db", "articles.json")
FEATURED_FILE = os.path.join(BASE_DIR, "db", "featured_products.json")
MAX_RESULTS = 5

def get_first_matching_articles(title, max_results=MAX_RESULTS):
    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except FileNotFoundError:
        logging.warning("Archivo de artículos no encontrado.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decodificando artículos: {e}")
        return []
    except Exception as e:
        logging.error(f"Error inesperado leyendo artículos: {e}")
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
    except FileNotFoundError:
        logging.warning(f"Archivo no encontrado: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decodificando {file_path}: {e}")
        return []
    except Exception as e:
        logging.error(f"Error inesperado leyendo {file_path}: {e}")
        return []

def save_json(file_path: str, data: list):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Datos guardados en {file_path}")
    except Exception as e:
        logging.error(f"Error guardando {file_path}: {e}")

def update_article_system(article_id: str, new_data: dict):
    try:
        articles = load_json(ARTICLES_FILE)
        updated = False
        for article in articles:
            if str(article.get("id")) == str(article_id):
                article.update(new_data)
                updated = True
                break
        if updated:
            save_json(ARTICLES_FILE, articles)
            logging.info(f"Artículo actualizado: {article_id}")
        else:
            logging.warning(f"Artículo no encontrado para actualizar: {article_id}")
        return updated
    except Exception as e:
        logging.error(f"Error actualizando artículo {article_id}: {e}")
        return False

def delete_article_system(article_id: str) -> bool:
    try:
        articles = load_json(ARTICLES_FILE)
        new_articles = [a for a in articles if str(a.get("id")) != str(article_id)]

        if len(new_articles) == len(articles):
            logging.warning(f"Artículo no encontrado para eliminar: {article_id}")
            return False  # no existía ese id

        save_json(ARTICLES_FILE, new_articles)
        logging.info(f"Artículo eliminado: {article_id}")
        return True
    except Exception as e:
        logging.error(f"Error eliminando artículo {article_id}: {e}")
        return False

def create_article_system(new_data: dict) -> dict:
    try:
        articles = load_json(ARTICLES_FILE)

        # Buscar el último id existente (ejemplo: MLA100001)
        if articles:
            existing_ids = [a.get("id", "") for a in articles if isinstance(a.get("id"), str) and a.get("id", "").startswith("MLA")]
            if existing_ids:
                last_num = max([int(e.replace("MLA", "")) for e in existing_ids])
                new_id = f"MLA{last_num + 1:06d}"
            else:
                new_id = "MLA100001"
        else:
            new_id = "MLA100001"

        new_article = {"id": new_id, **new_data}
        articles.append(new_article)

        save_json(ARTICLES_FILE, articles)
        logging.info(f"Artículo creado: {new_id}")
        return new_article
    except Exception as e:
        logging.error(f"Error creando artículo: {e}")
        return {}