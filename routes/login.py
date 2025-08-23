from flask import Blueprint, request
from process.auth_service import login_user

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username") if data else None
    password = data.get("password") if data else None

    response, status = login_user(username, password)
    return response, status
