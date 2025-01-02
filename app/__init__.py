"""Initialises and configures Flask, integrates Celery, and registers application blueprints."""

# Author: Alexander Hambley
# License: BSD 3-Clause

import os

from flask import Flask

from app.celery_worker import make_celery, celery
from app.ro_crates.routes import ro_crates_bp
from app.utils.config import DevelopmentConfig, ProductionConfig, make_celery


def create_app() -> Flask:
    """
    Create and configures Flask application.

    :return: Flask: A configured Flask application instance.
    """
    app = Flask(__name__)
    app.register_blueprint(ro_crates_bp, url_prefix="/ro_crates")

    # Load configuration:
    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        # Development environment:
        app.debug = True
        print("URL Map:")
        for rule in app.url_map.iter_rules():
            print(rule)
        app.config.from_object(DevelopmentConfig)

    # Integrate Celery
    make_celery(app)

    return app
