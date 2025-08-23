from flask import Blueprint, request
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
    data = request.get_json()
    username = data.get("username") if data else None
    password = data.get("password") if data else None

    response, status = register_user(username, password)
    return response, status
