import logging
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config.Config import Config

# Blueprints
from routes.get_by_title import get_by_title_bp
from routes.register import register_bp
from routes.get_all import get_all_bp 
from routes.login import login_bp
from routes.update_by_id import update_bp
from routes.delete_by_id import delete_bp
from routes.create import create_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Configuración de Swagger
    Swagger(app, config=app.config['SWAGGER_CONFIG'])

    # Registro de Blueprints
    blueprints = [
        get_by_title_bp,
        register_bp,
        get_all_bp,
        login_bp,
        update_bp,
        delete_bp,
        create_bp
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

    # Logging básico
    logging.basicConfig(level=logging.INFO)
    logging.info("App Flask inicializada correctamente.")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config['FLASK_DEBUG'])