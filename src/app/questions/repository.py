from uuid import uuid4
from src.app.models import QuestionModel


def fetch_questions():
    items = [e.to_dict() for e in QuestionModel.query().limit(10000)]
    return items

def add_question(question):
    question['id'] = str(uuid4())
    question = QuestionModel(**question)
    question.save()

def update_question(question_id, data):
    data['id'] = question_id
    question = QuestionModel.get(id=question_id)
    question.update(**data)
    question.save()

def remove_question(question_id):
    question = QuestionModel.get(id=question_id)
    question.delete()