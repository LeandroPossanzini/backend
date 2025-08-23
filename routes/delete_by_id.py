from flask import Blueprint, jsonify
from utils.auth import token_required
from process.articles_service import delete_article_process

delete_bp = Blueprint("delete_bp", __name__)

@delete_bp.route("/delete_by_id/<article_id>", methods=["DELETE"])
@token_required
def delete_by_id(article_id):
    result = delete_article_process(article_id)
    return jsonify(result), (200 if result["success"] else 404)
