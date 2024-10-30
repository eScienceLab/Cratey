import os

from flask import Flask

from app.ro_crates.routes import ro_crates_bp
from app.utils.config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ro_crates_bp, url_prefix="/ro_crates")

    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        # Development environment:
        print("URL Map:")
        for rule in app.url_map.iter_rules():
            print(rule)
        app.config.from_object(DevelopmentConfig)

    return app
