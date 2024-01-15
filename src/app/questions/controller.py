from flask import Blueprint, jsonify, request as req
from src.app.questions import repository
from src.middlewares import require_permission

blueprint = Blueprint('questions', __name__)

@blueprint.route('/questions', methods=['GET'])
def fetch_questions():
    """Fetch questions.
    ---
    tags:
        - questions
    responses:
        200:
            description: OK
    """
    return jsonify(data=repository.fetch_questions())

@blueprint.route('/questions', methods=['POST'])
@require_permission('create:questions')
def add_question():
    """Add question.
    ---
    tags:
        - questions
    responses:
        200:
            description: OK
    """
    question = req.get_json()
    repository.add_question(question)
    return jsonify(data=question)

@blueprint.route('/question/<question_id>', methods=['PUT'])
@require_permission('update:questions')
def update_question(question_id):
    """Update question.
    ---
    parameters:
        - name: question_id
          in: path
          type: string
          required: true
    tags:
        - questions
    responses:
        200:
            description: OK
    """
    data = req.get_json()
    repository.update_department(question_id, data)
    return jsonify(data=data)

@blueprint.route('/questions/<question_id>', methods=['DELETE'])
@require_permission('delete:questions')
def remove_question(question_id):
    """Remove question.
    ---
    parameters:
        - name: question_id
          in: path
          type: string
          required: true
    tags:
        - questions
    responses:
        200:
            description: OK
    """
    repository.remove_question(question_id)
    return jsonify(data={})
