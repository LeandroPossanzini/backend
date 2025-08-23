from flask import Flask, request
from flask_cors import CORS
from process.user_service import register_user
from routes.get_by_title import get_by_title_bp
from routes.register import register_bp

app = Flask(__name__)
CORS(app)


app.register_blueprint(get_by_title_bp)

app.register_blueprint(register_bp)

if __name__ == "__main__":
    app.run(debug=True)
