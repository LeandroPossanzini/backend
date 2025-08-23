from flask import Blueprint, request, jsonify
from utils.auth import token_required
from process.articles_service import create_article_process

create_bp = Blueprint("create_bp", __name__)

@create_bp.route("/create", methods=["POST"])
@token_required
def create_article():
    new_data = request.json
    if not new_data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    result = create_article_process(new_data)
    status_code = 201 if result["success"] else 400
    return jsonify(result), status_code
