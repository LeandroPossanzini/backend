import os

USERS_FILE = os.path.join("db", "users.txt")

def ensure_db_exists():
    os.makedirs("db", exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            pass  # crea archivo vacío

def get_all_users() -> list[dict]:
    ensure_db_exists()
    users = []
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            username, password = line.strip().split(",", 1)
            users.append({"username": username, "password": password})
    return users

def user_exists(username: str) -> bool:
    return any(u["username"] == username for u in get_all_users())

def save_user(username: str, password: str) -> bool:
    ensure_db_exists()
    if user_exists(username):
        return False
    with open(USERS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{username},{password}\n")
    return True
