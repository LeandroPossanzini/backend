import logging
from flask import Blueprint, request, jsonify
from process.most_searched import process_search

get_by_title_bp = Blueprint("get_by_title_bp", __name__)

@get_by_title_bp.route('/get_by_title', methods=['GET'])
def get_by_title():
    """
    Buscar artículos por título
    ---
    tags:
      - Artículos
    description: >
      Este endpoint permite buscar artículos que coincidan con un título parcial o completo.
      Puede ser accedido sin autenticación. Devuelve una lista de artículos con detalles completos.
    parameters:
      - name: title
        in: query
        type: string
        required: true
        description: Título del artículo a buscar
      - name: username
        in: query
        type: string
        required: false
        description: Nombre de usuario que realiza la búsqueda (opcional)
    responses:
      200:
        description: Lista de artículos encontrados
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              title:
                type: string
              description:
                type: string
              price:
                type: number
              currency:
                type: string
              images:
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
              payment_methods:
                type: array
                items:
                  type: string
      400:
        description: Parámetro title faltante
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: No se encontraron artículos
        schema:
          type: object
          properties:
            message:
              type: string
    """
    try:
        title = request.args.get("title", "").strip()
        username = request.args.get("username", "desconocido")
        if not title:
            return jsonify({"error": "Debe proveer un título"}), 400

        result = process_search(title, username)
        logging.info(f"Búsqueda de artículos por título: '{title}' por usuario: '{username}'")

        if not result:
            return jsonify({"message": "Artículo no encontrado"}), 404

        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error en búsqueda por título: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
