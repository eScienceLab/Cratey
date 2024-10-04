from flask import Blueprint, request, jsonify

ro_crates_bp = Blueprint('ro_crates', __name__)


@ro_crates_bp.route('/ro-crates/<id>', methods=['PUT'])
def put_ro_crate(id):
    data = request.get_json()
    return jsonify({'message': f'Crate {id} updated'}), 200