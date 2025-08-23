from system.user_repository import save_user

def register_user(username: str, password: str) -> tuple[dict, int]:
    """
    Lógica de registro de usuario.
    Devuelve (response_dict, status_code)
    """
    if not username or not password:
        return {"error": "Username and password are required"}, 400

    if not save_user(username, password):
        return {"error": f"User '{username}' already exists"}, 409

    return {"message": f"User {username} registered successfully!"}, 200
