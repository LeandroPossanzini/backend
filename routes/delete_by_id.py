import logging
from flask import Blueprint, jsonify
from utils.auth import token_required
from process.articles_service import delete_article_process

delete_bp = Blueprint("delete_bp", __name__)

@delete_bp.route("/delete_by_id/<article_id>", methods=["DELETE"])
@token_required
def delete_by_id(article_id):
    """
    Eliminar un artículo por ID
    ---
    tags:
      - Artículos
    description: >
      Permite eliminar un artículo existente. Se requiere token de autenticación.
    parameters:
      - name: article_id
        in: path
        type: string
        required: true
        description: ID del artículo a eliminar
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token JWT con formato "Bearer <token>"
    responses:
      200:
        description: Artículo eliminado correctamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Article deleted successfully."
            success:
              type: boolean
              example: true
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
        result = delete_article_process(article_id)
        logging.info(f"Intento de eliminación de artículo: {article_id}, resultado: {result}")

        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        logging.error(f"Error al eliminar artículo {article_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500
