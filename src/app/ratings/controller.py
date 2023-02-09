from flask import Blueprint, jsonify, request as req
from src.app.ratings import repository

blueprint = Blueprint('ratings', __name__)

@blueprint.route('/departments/<department_id>/professors/<professor_id>/ratings', methods=['GET'])
def fetch_professor_ratings(department_id, professor_id):
    """Fetch professor ratings.
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
        - ratings
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professor_ratings(department_id, professor_id))

@blueprint.route('/departments/<department_id>/professors/<professor_id>/ratings/summary', methods=['GET'])
def fetch_professor_rating_summary(department_id, professor_id):
    """Fetch professor rating summary.
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
        - ratings
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professor_rating_summary(department_id, professor_id))


@blueprint.route('/professors/<professor_id>/ratings/<student_id>', methods=['GET'])
def fetch_professor_ratings_by_student(professor_id, student_id):
    """Fetch professor ratings by student.
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
        - ratings
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_professor_ratings_by_student(professor_id, student_id))


@blueprint.route('/departments/<department_id>/professors/<professor_id>/ratings/<student_id>', methods=['POST'])
def rate_professor(department_id, professor_id, student_id):
    """Rate professor.
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
        - name: student_id
          in: path
          type: string
          required: true
        - name: ratings
          in: body
          type: object
          required: true
    tags:
        - ratings
    responses:
        200:
            description: OK
    """
    # Only the own user can rate a professor
    if(req.user is None or req.user.get('id', '') != student_id):
        return jsonify(error='Unauthorized'), 401

    ratings = req.get_json().get('ratings', {})
    comments = req.get_json().get('comments', {})
    return jsonify(data=repository.rate_professor(department_id, professor_id, student_id, ratings, comments))
    