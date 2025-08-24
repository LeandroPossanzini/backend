import logging
from system.analytics_repository import get_last_search_system

def get_last_search(username: str) -> str | None:
    if not isinstance(username, str) or not username.strip():
        logging.warning("Username inválido en get_last_search.")
        return None
    return get_last_search_system(username)