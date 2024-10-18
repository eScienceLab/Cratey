from flask import Blueprint, jsonify

ro_crates_bp = Blueprint('ro_crates', __name__)


@ro_crates_bp.route('/ro-crates/<id>', methods=['GET'])
def get_ro_crate(crate_id):
    crate = {'id': crate_id, 'crate': 'data'}
    return jsonify(crate), 200


@ro_crates_bp.route('/ro-crates', methods=['GET'])
def get_ro_crates():
    return jsonify([]), 200

