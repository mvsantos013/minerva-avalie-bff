from flask import Blueprint, jsonify, request as req
from src.app.disciplines import repository
from src.middlewares import require_permission

blueprint = Blueprint('disciplines', __name__)

@blueprint.route('/org/<organization_id>/disciplines', methods=['GET'])
def fetch_disciplines(organization_id):
    """Fetch disciplines.
    ---
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_disciplines(organization_id))

@blueprint.route('/org/<organization_id>/disciplines/<discipline_id>', methods=['GET'])
def fetch_discipline(organization_id, discipline_id):
    """Fetch discipline.
    ---
    parameters:
        - name: discipline_id
          in: path
          type: string
          required: true
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    discipline = repository.fetch_discipline(organization_id, discipline_id)
    return jsonify(data=discipline)

@blueprint.route('/org/<organization_id>/disciplines', methods=['POST'])
@require_permission('create:disciplines')
def add_discipline(organization_id):
    """Add discipline.
    ---
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    discipline = req.get_json()
    repository.add_discipline(organization_id, discipline)
    return jsonify(data=discipline)

@blueprint.route('/org/<organization_id>/disciplines/<discipline_id>', methods=['PUT'])
@require_permission('update:disciplines')
def update_discipline(organization_id, discipline_id):
    """Update discipline.
    ---
    parameters:
        - name: discipline_id
          in: path
          type: string
          required: true
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    data = req.get_json()
    repository.update_discipline(organization_id, discipline_id, data)
    return jsonify(data=data)

@blueprint.route('/org/<organization_id>/disciplines/<discipline_id>', methods=['DELETE'])
@require_permission('delete:disciplines')
def remove_discipline(organization_id, discipline_id):
    """Remove discipline.
    ---
    parameters:
        - name: discipline_id
          in: path
          type: string
          required: true
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    repository.remove_discipline(organization_id, discipline_id)
    return jsonify(data={})
