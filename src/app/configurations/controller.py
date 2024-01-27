from flask import Blueprint, jsonify, request as req
from src.app.configurations import repository
from src.middlewares import require_permission

blueprint = Blueprint('configurations', __name__)

@blueprint.route('/configurations', methods=['GET'])
def fetch_configurations():
    """Fetch configurations.
    ---
    tags:
        - configurations
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_configurations())

@blueprint.route('/configurations', methods=['POST'])
@require_permission('manage:configurations')
def add_configuration():
    """Add configuration.
    ---
    tags:
        - configurations
    responses:
        200:
            description: OK
    """
    configuration = req.get_json()
    repository.add_configuration(configuration)
    return jsonify(data=configuration)

@blueprint.route('/configurations/<configuration_id>', methods=['PUT'])
@require_permission('manage:configurations')
def update_configuration(configuration_id):
    """Update configuration.
    ---
    parameters:
        - name: configuration_id
          in: path
          type: string
          required: true
    tags:
        - configurations
    responses:
        200:
            description: OK
    """
    data = req.get_json()
    repository.update_configuration(configuration_id, data)
    return jsonify(data=data)

@blueprint.route('/configurations/<configuration_id>', methods=['DELETE'])
@require_permission('manage:configurations')
def remove_configuration(configuration_id):
    """Remove configuration.
    ---
    parameters:
        - name: configuration_id
          in: path
          type: string
          required: true
    tags:
        - configurations
    responses:
        200:
            description: OK
    """
    repository.remove_configuration(configuration_id)
    return jsonify(data={})
