from flask import Flask, request
from flask_cors import CORS
from process.user_service import register_user
from routes.get_by_title import get_by_title_bp
from routes.register import register_bp
from routes.get_all import get_all_bp 
from routes.login import login_bp
from routes.update_by_id import update_bp
from routes.delete_by_id import delete_bp
from routes.create import create_bp

app = Flask(__name__)
CORS(app)


app.register_blueprint(get_by_title_bp)

app.register_blueprint(register_bp)

app.register_blueprint(get_all_bp)

app.register_blueprint(login_bp)

app.register_blueprint(update_bp)

app.register_blueprint(delete_bp)

app.register_blueprint(create_bp)

if __name__ == "__main__":
    app.run(debug=True)
