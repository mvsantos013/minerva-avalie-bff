from flask import Blueprint, jsonify, request as req
from src.app.auth.groups import repository
from src.middlewares import require_permission

blueprint = Blueprint('groups', __name__)

@blueprint.route('/groups', methods=['GET'])
@require_permission('manage:groups')
def fetch_groups():
    """Fetch groups.
    ---
    tags:
        - groups
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_groups())

@blueprint.route('/groups', methods=['POST'])
@require_permission('manage:groups')
def create_group():
    """Create group.
    ---
    tags:
        - groups
    responses:
        200:
            description: OK
    """
    group = req.get_json()
    repository.create_group(group)
    return jsonify(data=group)

@blueprint.route('/groups/<group_id>', methods=['DELETE'])
@require_permission('manage:groups')
def delete_group(group_id):
    """Delete group.
    ---
    parameters:
        - name: group_id
          in: path
          type: string
          required: true
    tags:
        - groups
    responses:
        200:
            description: OK
    """
    repository.delete_group(group_id)
    return jsonify(data={})

@blueprint.route('/groups/<group_id>/permissions', methods=['GET'])
def fetch_group_permissions(group_id):
    """Fetch permissions.
    ---
    tags:
        - groups
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_group_permissions(group_id))

@blueprint.route('/groups/<group_id>/permissions', methods=['PUT'])
@require_permission('manage:groups-permissions')
def update_group_permissions(group_id):
    """Update group permissions.
    ---
    tags:
        - groups
    responses:
        200:
            description: OK
    """
    permissions_to_add = req.get_json()['permissionsToAdd']
    permissions_to_remove = req.get_json()['permissionsToRemove']
    repository.update_group_permissions(group_id, permissions_to_add, permissions_to_remove)
    return jsonify(data={'message': 'Permissions updated successfully'})
