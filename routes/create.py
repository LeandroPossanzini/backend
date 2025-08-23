from flask import Blueprint, request, jsonify
from utils.auth import token_required
from process.articles_service import create_article_process

create_bp = Blueprint("create_bp", __name__)

@create_bp.route("/create", methods=["POST"])
@token_required
def create_article():
    """
    Crear un nuevo artículo
    ---
    tags:
      - Artículos
    description: >
      Permite crear un nuevo artículo en el sistema. 
      Se requiere token de autenticación y enviar un JSON con todos los campos obligatorios.
    consumes:
      - application/json
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token JWT con formato "Bearer <token>"
      - in: body
        name: body
        required: true
        description: Datos del artículo a crear
        schema:
          type: object
          required:
            - title
            - description
            - price
            - currency
            - images
            - payment_methods
            - seller
            - additional_details
          properties:
            title:
              type: string
              example: "Nuevo artículo"
            description:
              type: string
              example: "Descripción del artículo"
            price:
              type: number
              example: 15999.99
            currency:
              type: string
              example: "ARS"
            images:
              type: array
              items:
                type: string
            payment_methods:
              type: array
              items:
                type: string
            seller:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                location:
                  type: string
                reputation:
                  type: string
                sales:
                  type: integer
            additional_details:
              type: object
              properties:
                category:
                  type: string
                rating:
                  type: number
                reviews:
                  type: integer
                stock:
                  type: integer
                warranty:
                  type: string
    responses:
      201:
        description: Artículo creado correctamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Article created successfully."
            success:
              type: boolean
              example: true
      400:
        description: Error en la creación (datos incompletos o inválidos)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No data provided"
            success:
              type: boolean
              example: false
    """
    new_data = request.json
    if not new_data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    result = create_article_process(new_data)
    status_code = 201 if result["success"] else 400
    return jsonify(result), status_code
