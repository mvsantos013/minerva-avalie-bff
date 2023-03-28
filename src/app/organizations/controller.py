from flask import Blueprint, jsonify, request as req
from src.app.organizations import repository
from src.middlewares import require_permission

blueprint = Blueprint('organizations', __name__)

@blueprint.route('/organizations', methods=['GET'])
def fetch_organizations():
    """Fetch organizations.
    ---
    tags:
        - organizations
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_organizations())

@blueprint.route('/organizations/<organization_id>', methods=['GET'])
def fetch_organization(organization_id):
    """Fetch organization.
    ---
    parameters:
        - name: organization_id
          in: path
          type: string
          required: true
    tags:
        - organizations
    responses:
        200:
            description: OK
    """
    organization = repository.fetch_organization(organization_id)
    return jsonify(data=organization)

@blueprint.route('/organizations', methods=['POST'])
@require_permission('create:organizations')
def add_organization():
    """Add organization.
    ---
    tags:
        - organizations
    responses:
        200:
            description: OK
    """
    organization = req.get_json()
    repository.add_organization(organization)
    return jsonify(data=organization)

@blueprint.route('/organizations/<organization_id>', methods=['PUT'])
@require_permission('update:organizations')
def update_organization(organization_id):
    """Update organization.
    ---
    parameters:
        - name: organization_id
          in: path
          type: string
          required: true
    tags:
        - organizations
    responses:
        200:
            description: OK
    """
    data = req.get_json()
    repository.update_organization(organization_id, data)
    return jsonify(data=data)

@blueprint.route('/organizations/<organization_id>', methods=['DELETE'])
@require_permission('delete:organizations')
def remove_organization(organization_id):
    """Remove organization.
    ---
    parameters:
        - name: organization_id
          in: path
          type: string
          required: true
    tags:
        - organizations
    responses:
        200:
            description: OK
    """
    repository.remove_organization(organization_id)
    return jsonify(data={})
