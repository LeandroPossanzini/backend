from flask import Blueprint, jsonify, request
from process.featured_service import fetch_all_featured
from utils.decode import decode_token
from process.last_serch_service import get_last_search
from process.most_searched import process_search

get_all_bp = Blueprint("get_all_bp", __name__)

@get_all_bp.route("/get_all", methods=["GET"])
def get_all():
    auth_header = request.headers.get("Authorization")  # Revisamos si envían Authorization
    token = None
    username = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1] 
        username = decode_token(token)

    if username:
        last_search = get_last_search(username)
        if last_search:
            print(f"Usuario {username} última búsqueda: {last_search}")
            products = process_search(last_search, username)
            return jsonify(products), 200

    # Si no hay token o no hay búsqueda previa → devolvemos destacados
    products = fetch_all_featured()
    return jsonify(products), 200
