from flask import Blueprint, jsonify, request as req
from src.app.testimonials import repository

blueprint = Blueprint('testimonials', __name__)

@blueprint.route('/professors/<professor_id>/testimonials', methods=['GET'])
def fetch_professor_testimonials(professor_id):
    """Fetch testimonials by professor.
    ---
    parameters:
        - name: professor_id
          in: query
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professor_testimonials(professor_id))

@blueprint.route('/testimonials', methods=['POST'])
def add_testimonial():
    """Add testimonial.
    ---
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    testimonial = req.get_json()
    repository.add_testimonial(testimonial)
    return jsonify(data=testimonial)

@blueprint.route('/professors/<professor_id>/testimonials/<student_id>', methods=['PUT'])
def update_testimonial(professor_id, student_id):
    """Update testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: student_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    data = req.get_json()
    repository.update_testimonial(professor_id, student_id, data)
    return jsonify(data=data)

@blueprint.route('/professors/<professor_id>/testimonials/<student_id>', methods=['DELETE'])
def remove_testimonial(professor_id, student_id):
    """Remove testimonial.
    ---
    parameters:
        - name: professor_id
          in: path
          type: string
          required: true
        - name: student_id
          in: path
          type: string
          required: true
    tags:
        - testimonials
    responses:
        200:
        description: OK
    """
    repository.remove_testimonial(professor_id, student_id)
    return jsonify(data={})
