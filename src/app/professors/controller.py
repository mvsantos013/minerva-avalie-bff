from flask import Blueprint, jsonify, request as req
from src.app.professors import repository
from src.middlewares import require_permission

blueprint = Blueprint('professors', __name__)

@blueprint.route('/professors', methods=['GET'])
def fetch_professors():
    """Fetch professors.
    ---
    tags:
        - professors
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professors())

@blueprint.route('/professors/<professor_id>', methods=['GET'])
def fetch_professor(professor_id):
    """Fetch professor.
    ---
    parameters:
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
    professor = repository.fetch_professor(professor_id)
    return jsonify(data=professor)


@blueprint.route('/professors/<professor_id>/disciplines', methods=['GET'])
def fetch_professor_disciplines(professor_id):
    """Fetch professors.
    ---
    parameters:
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
    return jsonify(data=repository.fetch_professor_disciplines(professor_id))

@blueprint.route('/professors/<professor_id>/testimonials/<discipline_id>', methods=['GET'])
def fetch_professor_testimonials(professor_id, discipline_id):
    """Fetch testimonials by professor.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: discipline_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professor_testimonials(discipline_id, professor_id))

@blueprint.route('/professors', methods=['POST'])
@require_permission('create:professors')
def add_professor():
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

@blueprint.route('/professors/<professor_id>', methods=['PUT'])
@require_permission('update:professors')
def update_professor(professor_id):
    """Update professor.
    ---
    parameters:
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

@blueprint.route('/professors/<professor_id>', methods=['DELETE'])
@require_permission('delete:professors')
def remove_professor(professor_id):
    """Remove professor.
    ---
    tags:
        - professors
    responses:
        200:
            description: OK
    """
    repository.remove_professor(professor_id)
    return jsonify(data={})

@blueprint.route('/professors/ratings/<discipline_id>/summary', methods=['GET'])
def fetch_professor_ratings_of_discipline(discipline_id):
    """Fetch professor ratings of discipline.
    ---
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professor_ratings_of_discipline(discipline_id))


@blueprint.route('/professors/<professor_id>/testimonials/<discipline_id>', methods=['DELETE'])
@require_permission('post:professor-testimonial')
def remove_professor_testimonial(professor_id, discipline_id):
    """Remove testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: discipline_id
          in: path
          type: string
          required: true
        - name: testimonial
          in: body
          type: object
          required: true
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    # Only the own user can remove its testimonial
    student_id = req.get_json().get('studentId', '')
    if(req.user is None or req.user.get('id', '') != student_id):
        return jsonify(error='Unauthorized'), 401

    testimonial = req.get_json()
    repository.remove_testimonial(testimonial)
    return jsonify(data={})

@blueprint.route('/professors/<professor_id>/testimonials/<discipline_id>/report', methods=['POST'])
def report_testimonial(professor_id, discipline_id):
    """Report testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: discipline_id
          in: path
          type: string
          required: true
        - name: testimonial
          in: body
          type: object
          required: true
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    testimonial = req.get_json()
    testimonial['disciplineIdProfessorId'] = f'{discipline_id}:{professor_id}'
    testimonial['professorId'] = professor_id
    testimonial['disciplineId'] = discipline_id
    testimonial = repository.report_testimonial(testimonial)
    return jsonify(data=testimonial)

@blueprint.route('/professors/testimonials/reported', methods=['GET'])
@require_permission('manage:testimonial-reports')
def fetch_reported_testimonials():
    """Fetch reported testimonials.
    ---
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_reported_testimonials())

@blueprint.route('/professors/<professor_id>/testimonials/<discipline_id>/reported/approve', methods=['POST'])
@require_permission('manage:testimonial-reports')
def approve_reported_testimonial(professor_id, discipline_id):
    """Approve reported testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: discipline_id
          in: path
          type: string
          required: true
        - name: testimonial
          in: body
          type: object
          required: true
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    testimonial = req.get_json()
    testimonial = repository.approve_reported_testimonial(testimonial)
    return jsonify(data=testimonial)

@blueprint.route('/professors/<professor_id>/testimonials/<discipline_id>/reported/remove', methods=['DELETE'])
@require_permission('manage:testimonial-reports')
def remove_reported_testimonial(professor_id, discipline_id):
    """Remove reported testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: discipline_id
          in: path
          type: string
          required: true
        - name: testimonial
          in: body
          type: object
          required: true
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    testimonial = req.get_json()
    testimonial = repository.remove_reported_testimonial(testimonial)
    return jsonify(data=testimonial)