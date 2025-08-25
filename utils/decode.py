import jwt
from process.auth_service import SECRET_KEY

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("username")
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None
