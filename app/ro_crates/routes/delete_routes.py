from flask import Blueprint, jsonify

ro_crates_bp = Blueprint('ro_crates', __name__)


@ro_crates_bp.route('/ro-crates/<id>', methods=['DELETE'])
def delete_ro_crate(id):
    return jsonify({'message': f'Crate {id} deleted'}), 200