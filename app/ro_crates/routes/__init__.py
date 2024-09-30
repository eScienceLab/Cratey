from flask import Blueprint

from app.ro_crates.routes.get_routes import ro_crates_bp as get_routes_bp
from app.ro_crates.routes.post_routes import ro_crates_bp as post_routes_bp
from app.ro_crates.routes.put_routes import ro_crates_bp as put_routes_bp
from app.ro_crates.routes.delete_routes import ro_crates_bp as delete_routes_bp

ro_crates_bp = Blueprint('ro_crates', __name__)

ro_crates_bp.register_blueprint(get_routes_bp)
ro_crates_bp.register_blueprint(post_routes_bp)
ro_crates_bp.register_blueprint(put_routes_bp)
ro_crates_bp.register_blueprint(delete_routes_bp)