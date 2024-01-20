from flask import Blueprint, jsonify, request as req
from src.app.professors.testimonials import repository
from src.middlewares import require_permission

blueprint = Blueprint('testimonials', __name__)

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