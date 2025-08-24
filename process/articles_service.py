import logging
from system.articles_repository import update_article_system, create_article_system
from process.featured_service import update_featured_process
from system.articles_repository import delete_article_system
from system.featured_repository import delete_featured_system

REQUIRED_FIELDS = [
    "title",
    "description",
    "price",
    "currency",
    "images",
    "payment_methods",
    "seller",
    "additional_details"
]

def validate_product_data(new_data: dict) -> (bool, str):
    for field in REQUIRED_FIELDS:
        if field not in new_data:
            return False, f"Missing required field: '{field}'"
        if not new_data[field]:
            return False, f"Field '{field}' cannot be empty."
    if not isinstance(new_data.get("price"), (int, float)):
        return False, "Field 'price' must be a number."
    if not isinstance(new_data.get("images"), list):
        return False, "Field 'images' must be a list."
    return True, ""

def update_article_process(article_id: str, new_data: dict) -> dict:
    try:
        valid, error_msg = validate_product_data(new_data)
        if not valid:
            logging.warning(f"Validación fallida al actualizar artículo {article_id}: {error_msg}")
            return {"success": False, "message": error_msg}

        filtered_data = {k: v for k, v in new_data.items() if k in REQUIRED_FIELDS}

        article_updated = update_article_system(article_id, filtered_data)
        featured_updated = update_featured_process(article_id, filtered_data)

        if not article_updated:
            logging.warning(f"Artículo no encontrado para actualizar: {article_id}")
            return {"success": False, "message": "Article not found."}

        msg = "Article updated successfully."
        if featured_updated:
            msg += " Featured product also updated."

        logging.info(f"Artículo actualizado: {article_id}")
        return {"success": True, "message": msg}
    except Exception as e:
        logging.error(f"Error actualizando artículo {article_id}: {e}")
        return {"success": False, "message": "Internal server error."}

def delete_article_process(article_id: str) -> dict:
    try:
        article_deleted = delete_article_system(article_id)
        featured_deleted = delete_featured_system(article_id)

        if not article_deleted:
            logging.warning(f"Artículo no encontrado para eliminar: {article_id}")
            return {"success": False, "message": "Article not found."}

        msg = "Article deleted successfully."
        if featured_deleted:
            msg += " Featured product also deleted."

        logging.info(f"Artículo eliminado: {article_id}")
        return {"success": True, "message": msg}
    except Exception as e:
        logging.error(f"Error eliminando artículo {article_id}: {e}")
        return {"success": False, "message": "Internal server error."}

def create_article_process(new_data: dict) -> dict:
    try:
        valid, error_msg = validate_product_data(new_data)
        if not valid:
            logging.warning(f"Validación fallida al crear artículo: {error_msg}")
            return {"success": False, "message": error_msg}

        filtered_data = {k: v for k, v in new_data.items() if k in REQUIRED_FIELDS}

        article_created = create_article_system(filtered_data)

        if not article_created:
            logging.error("Error creando artículo.")
            return {"success": False, "message": "Error creating article."}

        logging.info(f"Artículo creado: {article_created.get('id')}")
        return {"success": True, "message": "Article created successfully.", "article": article_created}
    except Exception as e:
        logging.error(f"Error creando artículo: {e}")
        return {"success": False, "message": "Internal server error."}