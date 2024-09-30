from flask import Blueprint, request, jsonify

ro_crates_bp = Blueprint('ro_crates', __name__)


@ro_crates_bp.route('/ro-crates', methods=['GET'])
def get_ro_crates():
    return jsonify([]), 200


@ro_crates_bp.route('/ro-crates:create', methods=['POST'])
def create_ro_crate():
    return jsonify({'message': 'Crate created'}), 200
