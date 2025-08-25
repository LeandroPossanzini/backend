import logging
from flask import Blueprint, request, jsonify
from process.auth_service import login_user

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    """
    Login de usuario
    ---
    tags:
      - Usuarios
    description: >
      Permite que un usuario existente inicie sesión. 
      Se debe enviar username y password en el cuerpo de la petición.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Credenciales del usuario
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: leandro2
            password:
              type: string
              example: "miPassword123"
    responses:
      200:
        description: Login exitoso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Login successful"
            token:
              type: string
              description: JWT para autenticación en otros endpoints
            user:
              type: string
              example: "leandro2"
      401:
        description: Credenciales inválidas
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Usuario o contraseña incorrectos"
      400:
        description: Datos incompletos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username y password son requeridos"
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username y password son requeridos"}), 400

        response, status = login_user(username, password)
        logging.info(f"Intento de login para usuario: {username}, status: {status}")
        return response, status
    except Exception as e:
        logging.error(f"Error en login de usuario: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
