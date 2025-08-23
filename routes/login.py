from flask import Blueprint, request
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
    data = request.get_json()
    username = data.get("username") if data else None
    password = data.get("password") if data else None

    response, status = login_user(username, password)
    return response, status
