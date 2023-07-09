from flask import Blueprint, jsonify, request as req
from src.app.professors import repository
from src.middlewares import require_permission

blueprint = Blueprint('professors', __name__)

@blueprint.route('/departments/<department_id>/professors', methods=['GET'])
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

@blueprint.route('/departments/<department_id>/professors/disciplines', methods=['GET'])
def fetch_professors_disciplines(department_id):
    """Fetch professors disciplines.
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
    return jsonify(data=repository.fetch_professors_disciplines())


@blueprint.route('/departments/<department_id>/professors/<professor_id>/disciplines', methods=['GET'])
def fetch_professor_disciplines(department_id, professor_id):
    """Fetch professors by department.
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
    return jsonify(data=repository.fetch_professor_disciplines(department_id, professor_id))

@blueprint.route('/departments/<deparment_id>/professors', methods=['POST'])
@require_permission('create:professors')
def add_professor(deparment_id):
    """Add professor.
    ---
    tags:
        - professors
    responses:
        200:
            description: OK
    """
    professor = req.form.to_dict()
    professor['picture'] = req.files.get('picture')
    
    for prop in professor:
        if(professor[prop] == 'null'):
            professor[prop] = None

    allowed_image_extensions = ['png', 'jpg', 'jpeg']
    if professor['picture'] and professor['picture'].filename.split('.')[-1] not in allowed_image_extensions:
        return jsonify(error='Invalid image extension'), 400
    
    repository.add_professor(professor)
    return jsonify(data=professor)

@blueprint.route('/departments/<department_id>/professors/<professor_id>', methods=['PUT'])
@require_permission('update:professors')
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
    professor = req.form.to_dict()
    professor['picture'] = req.files.get('picture', None)
    
    for prop in professor:
        if(professor[prop] == 'null'):
            professor[prop] = None

    allowed_image_extensions = ['png', 'jpg', 'jpeg']
    if professor['picture'] and professor['picture'].filename.split('.')[-1] not in allowed_image_extensions:
        return jsonify(error='Invalid image extension'), 400
    
    repository.update_professor(professor_id, professor)
    return jsonify(data=professor)

@blueprint.route('/departments/<department_id>/professors/<professor_id>', methods=['DELETE'])
@require_permission('delete:professors')
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
