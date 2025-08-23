from system.analytics_repository import get_last_search_system

def get_last_search(username: str) -> str | None:
    return get_last_search_system(username)