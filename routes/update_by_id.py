from flask import Blueprint, request, jsonify
from utils.auth import token_required
from process.articles_service import update_article_process

update_bp = Blueprint("update_bp", __name__)

@update_bp.route("/update_by_id/<article_id>", methods=["PUT"])
@token_required
def update_by_id(article_id):
    new_data = request.json
    if not new_data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    result = update_article_process(article_id, new_data)
    print(result)
    status_code = 200 if result["success"] else 404
    return jsonify(result), status_code
