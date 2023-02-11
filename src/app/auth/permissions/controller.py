from flask import Blueprint, jsonify, request as req
from src.app.auth.permissions import repository
from src.middlewares import require_permission

blueprint = Blueprint('permissions', __name__)

@blueprint.route('/permissions', methods=['GET'])
@require_permission('manage:permissions')
def fetch_permissions():
    """Fetch permissions.
    ---
    tags:
        - permissions
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_permissions())

@blueprint.route('/permissions', methods=['POST'])
@require_permission('manage:permissions')
def create_permission():
    """Create permission.
    ---
    tags:
        - permissions
    responses:
        200:
            description: OK
    """
    permission = req.get_json()
    repository.create_permission(permission)
    return jsonify(data=permission)

@blueprint.route('/permissions/<permission_id>', methods=['DELETE'])
@require_permission('manage:permissions')
def delete_permission(permission_id):
    """Delete permission.
    ---
    parameters:
        - name: permission_id
          in: path
          type: string
          required: true
    tags:
        - permissions
    responses:
        200:
            description: OK
    """
    repository.delete_permission(permission_id)
    return jsonify(data={})
