import jwt
import datetime
from system.user_repository import get_all_users

# Clave secreta para firmar JWT (en producción usar variable de entorno)
SECRET_KEY = "mi_clave_secreta"

def login_user(username: str, password: str) -> tuple[dict, int]:
    """
    Lógica de login de usuario con JWT.
    Devuelve (response_dict, status_code)
    """
    if not username or not password:
        return {"error": "Username and password are required"}, 400

    users = get_all_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            # Generar token JWT
            payload = {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expira en 1 hora
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return {
                "message": "Login successful",
                "user": username,
                "token": token
            }, 200

    return {"error": "Invalid username or password"}, 401
