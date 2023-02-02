from flask import Blueprint, jsonify, request as req
from src.app.professors import repository

blueprint = Blueprint('professors', __name__)

@blueprint.route('/departments/<department_id/professors', methods=['GET'])
def fetch_professors_by_department(department_id):
    """Fetch professors by department.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
    tags:
        - professors
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professors_by_department(department_id))

@blueprint.route('/departments/<department_id>/professors/<professor_id>', methods=['GET'])
def fetch_professor(department_id, professor_id):
    """Fetch professor.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
        - name: professor_id
          in: path
          type: string
          required: true
    tags:
        - professors
    responses:
        200:
            description: OK
    """
    professor = repository.fetch_professor(department_id, professor_id)
    return jsonify(data=professor)

@blueprint.route('/departments/<deparment_id>/professors', methods=['POST'])
def add_professor(deparment_id):
    """Add professor.
    ---
    tags:
        - professors
    responses:
        200:
        description: OK
    """
    professor = req.get_json()
    repository.add_professor(professor)
    return jsonify(data=professor)

@blueprint.route('/department_id/<department_id>/professors/<professor_id>', methods=['PUT'])
def update_professor(department_id, professor_id):
    """Update professor.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
        - name: professor_id
          in: path
          type: string
          required: true
    tags:
        - professors
    responses:
        200:
        description: OK
    """
    data = req.get_json()
    repository.update_professor(professor_id, data)
    return jsonify(data=data)

@blueprint.route('/departments/<department_id>/professors/<professor_id>', methods=['DELETE'])
def remove_professor(department_id, professor_id):
    """Remove professor.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
    tags:
        - professors
    responses:
        200:
        description: OK
    """
    repository.remove_professor(department_id, professor_id)
    return jsonify(data={})
