from flask import Blueprint

from app.ro_crates.routes.post_routes import post_routes_bp

ro_crates_bp = Blueprint("ro_crates", __name__)

ro_crates_bp.register_blueprint(post_routes_bp, url_prefix="/post")
