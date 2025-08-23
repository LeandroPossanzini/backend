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
        if field in new_data:
            if not new_data[field]:
                return False, f"Field '{field}' cannot be empty."
        else:
            return False, f"Missing required field: '{field}'"


    return True, ""

def update_article_process(article_id: str, new_data: dict) -> dict:
    valid, error_msg = validate_product_data(new_data)
    if not valid:
        return {"success": False, "message": error_msg}

    # Solo conservar campos permitidos antes de actualizar
    filtered_data = {k: v for k, v in new_data.items() if k in REQUIRED_FIELDS}

    article_updated = update_article_system(article_id, filtered_data)
    featured_updated = update_featured_process(article_id, filtered_data)

    if not article_updated:
        return {"success": False, "message": "Article not found."}

    msg = "Article updated successfully."
    if featured_updated:
        msg += " Featured product also updated."

    return {"success": True, "message": msg}

def delete_article_process(article_id: str) -> dict:
    article_deleted = delete_article_system(article_id)
    featured_deleted = delete_featured_system(article_id)

    if not article_deleted:
        return {"success": False, "message": "Article not found."}

    msg = "Article deleted successfully."
    if featured_deleted:
        msg += " Featured product also deleted."

    return {"success": True, "message": msg}

def create_article_process(new_data: dict) -> dict:
    valid, error_msg = validate_product_data(new_data)
    if not valid:
        return {"success": False, "message": error_msg}

    # filtrar solo campos permitidos
    filtered_data = {k: v for k, v in new_data.items() if k in REQUIRED_FIELDS}

    article_created = create_article_system(filtered_data)

    if not article_created:
        return {"success": False, "message": "Error creating article."}

    return {"success": True, "message": "Article created successfully.", "article": article_created}