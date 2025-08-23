from system.featured_repository import get_all_featured, update_featured

def fetch_all_featured() -> list:
    return get_all_featured()

def update_featured_process(article_id: str, new_data: dict) -> bool:
    return update_featured(article_id, new_data)

