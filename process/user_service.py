import logging
from system.user_repository import save_user

def register_user(username: str, password: str) -> tuple[dict, int]:
    if not username or not password:
        logging.warning("Intento de registro con datos incompletos.")
        return {"error": "Username and password are required"}, 400

    if " " in username or len(username) < 3:
        logging.warning(f"Intento de registro con username inválido: {username}")
        return {"error": "Invalid username format"}, 400

    if len(password) < 3:
        logging.warning(f"Intento de registro con contraseña débil para usuario: {username}")
        return {"error": "Password must be at least 3 characters"}, 400

    if not save_user(username, password):
        logging.info(f"Intento de registro para usuario existente: {username}")
        return {"error": "User already exists"}, 409

    logging.info(f"Usuario registrado exitosamente: {username}")
    return {"message": f"User {username} registered successfully!"}, 201