from flask import Flask, request
from flask_cors import CORS
from process.user_service import register_user

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username") if data else None
    password = data.get("password") if data else None

    # Delegamos la lógica al servicio
    response, status = register_user(username, password)
    return response, status


if __name__ == "__main__":
    app.run(debug=True)
