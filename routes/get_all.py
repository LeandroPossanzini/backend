from flask import Blueprint, jsonify, request
from process.featured_service import fetch_all_featured

get_all_bp = Blueprint("get_all_bp", __name__)

@get_all_bp.route("/get_all", methods=["GET"])
def get_all():
    auth_header = request.headers.get("Authorization")  # Revisamos si envían Authorization
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]  
    
    products = fetch_all_featured()  
    return jsonify(products), 200
