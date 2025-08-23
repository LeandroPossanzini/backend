from flask import Blueprint, request
from process.user_service import register_user

register_bp = Blueprint("register_bp", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username") if data else None
    password = data.get("password") if data else None

    response, status = register_user(username, password)
    return response, status
