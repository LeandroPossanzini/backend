from flask import Blueprint, jsonify, request
from process.featured_service import fetch_all_featured
from utils.decode import decode_token
from process.last_serch_service import get_last_search
from process.most_searched import process_search

get_all_bp = Blueprint("get_all_bp", __name__)

@get_all_bp.route("/get_all", methods=["GET"])
def get_all():
    """
    Obtener productos destacados o por última búsqueda
    ---
    tags:
      - Productos
    description: >
      Este endpoint devuelve una lista de productos. 
      - Si se envía un token de autorización válido y el usuario tiene una última búsqueda registrada, se devuelven los productos que coinciden con esa búsqueda.
      - Si no se envía token o no hay búsqueda previa, se devuelven los productos destacados.
      No requiere autenticación para acceder.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: false
        description: Token JWT con formato "Bearer <token>"
    responses:
      200:
        description: Lista de productos
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
    """
    auth_header = request.headers.get("Authorization")  # Revisamos si envían Authorization
    token = None
    username = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1] 
        username = decode_token(token)

    if username:
        last_search = get_last_search(username)
        if last_search:
            products = process_search(last_search, username)
            return jsonify(products), 200

    # Si no hay token o no hay búsqueda previa → devolvemos destacados
    products = fetch_all_featured()
    return jsonify(products), 200
