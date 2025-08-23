from flask import Blueprint, jsonify
from process.featured_service import fetch_all_featured

get_all_bp = Blueprint("get_all_bp", __name__)

@get_all_bp.route("/get_all", methods=["GET"])
def get_all():
    products = fetch_all_featured()
    return jsonify(products), 200
