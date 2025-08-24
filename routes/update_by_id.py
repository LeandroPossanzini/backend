import logging
from flask import Blueprint, request, jsonify
from utils.auth import token_required
from process.articles_service import update_article_process

update_bp = Blueprint("update_bp", __name__)

@update_bp.route("/update_by_id/<article_id>", methods=["PUT"])
@token_required
def update_by_id(article_id):
    """
    Actualizar un artículo por ID
    ---
    tags:
      - Artículos
    description: >
      Permite actualizar un artículo existente. Se requiere token de autenticación.
      Debe enviarse un JSON con todos los campos obligatorios del artículo.
    parameters:
      - name: article_id
        in: path
        type: string
        required: true
        description: ID del artículo a actualizar
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token JWT con formato "Bearer <token>"
      - in: body
        name: body
        required: true
        description: Datos del artículo a actualizar
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
              example: "Nuevo título del artículo"
            description:
              type: string
              example: "Descripción actualizada del artículo"
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
      200:
        description: Artículo actualizado correctamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Article updated successfully."
            success:
              type: boolean
              example: true
      400:
        description: No se proporcionaron datos
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No data provided"
            success:
              type: boolean
              example: false
      404:
        description: Artículo no encontrado
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Article not found"
            success:
              type: boolean
              example: false
    """
    try:
        new_data = request.get_json()
        if not new_data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        # Validación básica de campos obligatorios
        required_fields = ["title", "description", "price", "currency", "images", "payment_methods", "seller", "additional_details"]
        missing = [field for field in required_fields if field not in new_data]
        if missing:
            return jsonify({"success": False, "message": f"Missing fields: {', '.join(missing)}"}), 400

        result = update_article_process(article_id, new_data)
        logging.info(f"Update result for {article_id}: {result}")

        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        logging.error(f"Error updating article {article_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500
