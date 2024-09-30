import os

from flask import Flask

from app.ro_crates.routes import ro_crates_bp
from config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ro_crates_bp)

    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    return app
