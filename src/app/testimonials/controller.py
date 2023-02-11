from flask import Blueprint, jsonify, request as req
from src.app.testimonials import repository
from src.middlewares import require_permission

blueprint = Blueprint('testimonials', __name__)

@blueprint.route('/professors/<professor_id>/testimonials', methods=['GET'])
def fetch_professor_testimonials(professor_id):
    """Fetch testimonials by professor.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: departmentId
          in: query
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    department_id = req.args.get('departmentId', '')
    return jsonify(data=repository.fetch_professor_testimonials(department_id, professor_id))

@blueprint.route('/professors/<professor_id>/testimonials', methods=['POST'])
@require_permission('post:professor-testimonial')
def add_professor_testimonial(professor_id):
    """Add testimonial.
    ---
    parameters:
        - name: professor_id
            in: path
            type: string
            required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    # Only the own user can post a testimonial
    student_id = req.get_json().get('studentId', '')
    if(req.user is None or req.user.get('id', '') != student_id):
        return jsonify(error='Unauthorized'), 401

    testimonial = req.get_json().get('text', '')

    if(len(testimonial.replace(' ', '')) < 6):
        return jsonify(error='Depoimento deve ter ao menos 6 caracteres.'), 400

    testimonial = repository.add_testimonial(req.get_json())
    return jsonify(data=testimonial)

@blueprint.route('/professors/<professor_id>/testimonials/<testimonial_id>', methods=['PUT'])
@require_permission('post:professor-testimonial')
def update_professor_testimonial(professor_id, testimonial_id):
    """Update testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: testimonial_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    # Only the own user can update it's testimonial
    student_id = req.get_json().get('studentId', '')
    if(req.user is None or req.user.get('id', '') != student_id):
        return jsonify(error='Unauthorized'), 401

    text = req.get_json().get('text', '')

    if(len(text.replace(' ', '')) < 6):
        return jsonify(error='Depoimento deve ter ao menos 6 caracteres.'), 400

    testimonial = repository.update_testimonial(professor_id, testimonial_id, text)
    return jsonify(data=testimonial)

@blueprint.route('/professors/<professor_id>/testimonials/<testimonial_id>', methods=['DELETE'])
@require_permission('post:professor-testimonial')
def remove_professor_testimonial(professor_id, testimonial_id):
    """Remove testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: testimonial_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    # Only the own user can remove it's testimonial
    student_id = req.get_json().get('studentId', '')
    if(req.user is None or req.user.get('id', '') != student_id):
        return jsonify(error='Unauthorized'), 401

    repository.remove_testimonial(professor_id, testimonial_id)
    return jsonify(data={})

@blueprint.route('/professors/<professor_id>/testimonials/<testimonial_id>/report', methods=['POST'])
def report_testimonial(professor_id, testimonial_id):
    """Report testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: testimonial_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    testimonial = req.get_json()
    testimonial['professorId'] = professor_id
    testimonial['id'] = testimonial_id
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

@blueprint.route('/professors/<professor_id>/testimonials/reported/<testimonial_id>/approve', methods=['POST'])
@require_permission('manage:testimonial-reports')
def approve_reported_testimonial(professor_id, testimonial_id):
    """Approve reported testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: testimonial_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    testimonial = repository.approve_reported_testimonial(professor_id, testimonial_id)
    return jsonify(data=testimonial)

@blueprint.route('/professors/<professor_id>/testimonials/reported/<testimonial_id>/remove', methods=['DELETE'])
@require_permission('manage:testimonial-reports')
def remove_reported_testimonial(professor_id, testimonial_id):
    """Remove reported testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: testimonial_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    testimonial = repository.remove_reported_testimonial(professor_id, testimonial_id)
    return jsonify(data=testimonial)