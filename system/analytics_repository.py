ANALYTICS_FILE = "db/analytics.txt"

def save_analytics(username, search_word):
    if not username:
        username = "desconocido"
    with open(ANALYTICS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username} searched: {search_word}\n")
