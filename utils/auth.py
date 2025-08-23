from functools import wraps
from flask import request, jsonify
import jwt
from process.auth_service import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            token = token.split()[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify({"error": "Token is invalid"}), 401
        return f(*args, **kwargs)
    return decorated