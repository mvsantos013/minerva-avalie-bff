from flask import Blueprint, jsonify, request as req
from src.app.departments import repository
from src.middlewares import require_permission

blueprint = Blueprint('departments', __name__)

@blueprint.route('/departments', methods=['GET'])
def fetch_departments():
    """Fetch departments.
    ---
    tags:
        - departments
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_departments())

@blueprint.route('/departments/<department_id>', methods=['GET'])
def fetch_department(department_id):
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
    department = repository.fetch_department(department_id)
    return jsonify(data=department)

@blueprint.route('/departments', methods=['POST'])
@require_permission('create:departments')
def add_department():
    """Add department.
    ---
    tags:
        - departments
    responses:
        200:
            description: OK
    """
    department = req.get_json()
    repository.add_department(department)
    return jsonify(data=department)

@blueprint.route('/departments/<department_id>', methods=['PUT'])
@require_permission('update:departments')
def update_department(department_id):
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
    repository.update_department(department_id, data)
    return jsonify(data=data)

@blueprint.route('/departments/<department_id>', methods=['DELETE'])
@require_permission('delete:departments')
def remove_department(department_id):
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
    repository.remove_department(department_id)
    return jsonify(data={})
