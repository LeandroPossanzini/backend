import logging
from system.featured_repository import get_all_featured, update_featured

def fetch_all_featured() -> list:
    return get_all_featured()

def update_featured_process(article_id: str, new_data: dict) -> bool:
    if not isinstance(article_id, str) or not article_id.strip():
        logging.warning("ID de artículo inválido en update_featured_process.")
        return False
    if not isinstance(new_data, dict) or not new_data:
        logging.warning("Datos nuevos inválidos en update_featured_process.")
        return False
    try:
        return update_featured(article_id, new_data)
    except Exception as e:
        logging.error(f"Error actualizando producto destacado {article_id}: {e}")
        return False
