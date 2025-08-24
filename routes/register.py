import logging
from flask import Blueprint, request, jsonify
from process.user_service import register_user

register_bp = Blueprint("register_bp", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    description: >
      Permite registrar un nuevo usuario en el sistema. 
      Se debe enviar username y password en el cuerpo de la petición.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Datos del usuario a registrar
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: leandro148
            password:
              type: string
              example: "miPassword123"
    responses:
      200:
        description: Usuario registrado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User leandro148 registered successfully!"
      400:
        description: Datos incompletos o inválidos
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

        if len(password) < 3:
            return jsonify({"error": "La contraseña debe tener al menos 3 caracteres"}), 400

        response, status = register_user(username, password)
        logging.info(f"Intento de registro para usuario: {username}, status: {status}")
        return response, status if status != 200 else 201
    except Exception as e:
        logging.error(f"Error en registro de usuario: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
