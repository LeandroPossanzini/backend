from system.user_repository import get_all_users

def login_user(username: str, password: str) -> tuple[dict, int]:
    """
    Lógica de login de usuario.
    Devuelve (response_dict, status_code)
    """
    if not username or not password:
        return {"error": "Username and password are required"}, 400

    users = get_all_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return {"message": f"Login successful", "user": user["username"]}, 200

    return {"error": "Invalid username or password"}, 401