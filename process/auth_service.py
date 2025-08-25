import jwt
from datetime import datetime, timedelta, timezone
import logging
import os
from system.user_repository import get_all_users

SECRET_KEY = "mi_clave_secreta"

def login_user(username: str, password: str) -> tuple[dict, int]:
    try:
        if not username or not password:
            logging.warning("Intento de login con datos incompletos.")
            return {"error": "Username and password are required"}, 400

        users = get_all_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                try:
                    payload = {
                        "username": username,
                        "exp": datetime.now(timezone.utc) + timedelta(hours=1)  
                    }
                    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                except Exception as e:
                    logging.error(f"Error generando token JWT: {e}")
                    return {"error": "Internal server error"}, 500

                logging.info(f"Login exitoso para usuario: {username}")
                return {
                    "message": "Login successful",
                    "user": username,
                    "token": token
                }, 200

        logging.warning(f"Intento de login fallido para usuario: {username}")
        return {"error": "Invalid username or password"}, 401
    except Exception as e:
        logging.error(f"Error inesperado en login_user: {e}")
        return {"error": "Internal server error"}, 500
