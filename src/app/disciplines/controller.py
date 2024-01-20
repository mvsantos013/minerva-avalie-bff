from flask import Blueprint, jsonify, request as req
from src.app.disciplines import repository
from src.middlewares import require_permission

blueprint = Blueprint('disciplines', __name__)

@blueprint.route('/departments/<department_id>/disciplines', methods=['GET'])
def fetch_disciplines(department_id):
    """Fetch disciplines.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_disciplines(department_id))

@blueprint.route('/departments/<department_id>/disciplines/<discipline_id>', methods=['GET'])
def fetch_discipline(department_id, discipline_id):
    """Fetch discipline.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
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
    discipline = repository.fetch_discipline(department_id, discipline_id)
    return jsonify(data=discipline)


@blueprint.route('/departments/<department_id>/disciplines/<discipline_id>/professors', methods=['GET'])
def fetch_discipline_professors(department_id, discipline_id):
    """Fetch discipline.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
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
    professors = repository.fetch_discipline_professors(department_id, discipline_id)
    return jsonify(data=professors)

@blueprint.route('/departments/<department_id>/disciplines/<discipline_id>/testimonials', methods=['GET'])
def fetch_discipline_testimonials(department_id, discipline_id):
    """Fetch discipline.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
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
    testimonials = repository.fetch_discipline_testimonials(department_id, discipline_id)
    return jsonify(data=testimonials)

@blueprint.route('/departments/<department_id>/disciplines', methods=['POST'])
@require_permission('create:disciplines')
def add_discipline(department_id):
    """Add discipline.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    discipline = req.get_json()
    repository.add_discipline(department_id, discipline)
    return jsonify(data=discipline)

@blueprint.route('/departments/<department_id>/disciplines/<discipline_id>', methods=['PUT'])
@require_permission('update:disciplines')
def update_discipline(department_id, discipline_id):
    """Update discipline.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
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
    repository.update_discipline(department_id, discipline_id, data)
    return jsonify(data=data)

@blueprint.route('/departments/<department_id>/disciplines/<discipline_id>', methods=['DELETE'])
@require_permission('delete:disciplines')
def remove_discipline(department_id, discipline_id):
    """Remove discipline.
    ---
    parameters:
        - name: department_id
          in: path
          type: string
          required: true
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
    repository.remove_discipline(department_id, discipline_id)
    return jsonify(data={})

@blueprint.route('/disciplines/evaluation', methods=['POST'])
@require_permission('rate:place-evaluation')
def post_evaluation():
    """Post evaluation.
    ---
    parameters:
        - name: data
          in: body
          type: object
          required: true
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    data = req.get_json()
    repository.post_evaluation(data, req.user)
    return jsonify(data={'msg': 'success'})

@blueprint.route('/disciplines/<discipline_id>/evaluation', methods=['GET'])
def fetch_student_evaluation(discipline_id):
    """Fetch own evaluation.
    ---
    parameters:
        - name: professor_id
          in: query
          type: string
          required: true
        - name: period
          in: query
          type: string
          required: true
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    professor_id = req.args.get('professor_id')
    period = req.args.get('period')
    student_id = req.user['id']
    evaluation = repository.fetch_student_evaluation(discipline_id, professor_id, period, student_id)
    return jsonify(data=evaluation)

@blueprint.route('/disciplines/<discipline_id>/ratings/summary', methods=['GET'])
def fetch_discipline_ratings(discipline_id):
    """Fetch discipline ratings.
    ---
    tags:
        - disciplines
    responses:
        200:
            description: OK
    """
    evaluation = repository.fetch_discipline_ratings(discipline_id)
    return jsonify(data=evaluation)
