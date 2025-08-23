import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS_FILE = os.path.join(BASE_DIR, "db", "analytics.txt")

def get_last_search_system(username: str) -> str | None:
    if not os.path.exists(ANALYTICS_FILE):
        return None
    
    with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Buscamos la última entrada del usuario
    for line in reversed(lines):
        if line.startswith(username + " searched:"):
            return line.split("searched:")[1].strip()
    return None

def save_analytics_system(username: str, search_word: str):
    if not username:
        username = "desconocido"
    os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
    with open(ANALYTICS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username} searched: {search_word}\n")
