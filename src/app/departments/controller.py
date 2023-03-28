from flask import Blueprint, jsonify, request as req
from src.app.departments import repository
from src.middlewares import require_permission

blueprint = Blueprint('departments', __name__)

@blueprint.route('/org/<organization_id>/departments', methods=['GET'])
def fetch_departments(organization_id):
    """Fetch departments.
    ---
    tags:
        - departments
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_departments(organization_id))

@blueprint.route('/org/<organization_id>/departments/<department_id>', methods=['GET'])
def fetch_department(organization_id, department_id):
    """Fetch department.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
    tags:
        - departments
    responses:
        200:
            description: OK
    """
    department = repository.fetch_department(organization_id, department_id)
    return jsonify(data=department)

@blueprint.route('/org/<organization_id>/departments', methods=['POST'])
@require_permission('create:departments')
def add_department(organization_id):
    """Add department.
    ---
    tags:
        - departments
    responses:
        200:
            description: OK
    """
    department = req.get_json()
    repository.add_department(organization_id, department)
    return jsonify(data=department)

@blueprint.route('/org/<organization_id>/departments/<department_id>', methods=['PUT'])
@require_permission('update:departments')
def update_department(organization_id, department_id):
    """Update department.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
    tags:
        - departments
    responses:
        200:
            description: OK
    """
    data = req.get_json()
    repository.update_department(organization_id, department_id, data)
    return jsonify(data=data)

@blueprint.route('/org/<organization_id>/departments/<department_id>', methods=['DELETE'])
@require_permission('delete:departments')
def remove_department(organization_id, department_id):
    """Remove department.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
    tags:
        - departments
    responses:
        200:
            description: OK
    """
    repository.remove_department(organization_id, department_id)
    return jsonify(data={})
