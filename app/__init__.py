from flask import Flask
from app.configs.logging_config import setup_logging
# App Factory


def create_app():
    app = Flask(__name__)
    # app.config.from_object('configs.logging_config')

    # Initialize SocketIO with the app
    setup_logging()

    # Import and register your blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
