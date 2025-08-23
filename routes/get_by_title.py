from flask import Blueprint, request, jsonify
from process.most_searched import process_search

get_by_title_bp = Blueprint("get_by_title_bp", __name__)

@get_by_title_bp.route('/get_by_title', methods=['GET'])
def get_by_title():
    title = request.args.get("title")
    username = request.args.get("username", "desconocido")
    print(username)
    if not title:
        return jsonify({"error": "Debe proveer un título"}), 400

    result = process_search(title, username)

    if not result:
        return jsonify({"message": "Artículo no encontrado"}), 404

    return jsonify(result), 200
