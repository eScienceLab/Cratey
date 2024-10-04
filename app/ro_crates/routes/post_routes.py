from flask import Blueprint, request, jsonify

ro_crates_bp = Blueprint('ro_crates', __name__)


@ro_crates_bp.route('/ro-crates:create', methods=['POST'])
def create_ro_crate():
    return jsonify({'message': 'Crate created'}), 200


@ro_crates_bp.route('/ro-crates:create_from_tes', methods=['POST'])
def create_ro_crate_from_tes():
    data = request.get_json()
    return jsonify({'message': 'Crate created from TES package'}), 200


@ro_crates_bp.route('/ro-crates/<id>:add_files', methods=['POST'])
def add_files_to_ro_crate(id):
    data = request.get_json()
    return jsonify({'message': f'Files added to crate {id}'}), 200