from flask import request as req
from datetime import datetime, timezone
from src.lib import utils
from src.app.professors.models import ProfessorModel
from src.app.professors.ratings.models import ProfessorRatingModel

def fetch_professor_ratings(department_id, professor_id):
    """Fetch professor ratings."""
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')
    if(professor.publicRating is False and not utils.user_has_group('Admin')):
        return []
    ratings = []
    for e in ProfessorRatingModel.query(professorId=professor_id).limit(10000):
        rating = e.to_dict()
        if(req.user is None or req.user.get('id') != rating['studentId']):
            del rating['studentId'] # Remove student reference from response
        ratings.append(rating)
    return ratings

def fetch_professor_rating_summary(deparment_id, professor_id):
    professor = ProfessorModel.get(deparmentId=deparment_id, professorId=professor_id)
    if(professor is None):
        return {}
    if(professor.publicRating is False and not utils.user_has_group('Admin')):
        return {}
    return professor.ratingSummary

def fetch_professor_ratings_by_student(professor_id, student_id):
    ratings = ProfessorRatingModel.ByStudentId.query(studentId=student_id).limit(10000)
    if(ratings is None):
        return []
    return [r.to_dict() for r in ratings]

def rate_professor(department_id, professor_id, student_id, params):
    ratings = params.get('ratings')
    comments = params.get('comments')
    period = params.get('period')
    disciplineId = params.get('disciplineId')

    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')

    id = f'{disciplineId}:{period}:{student_id}'
    rating = ProfessorRatingModel.get(professorId=professor_id, id=id)
    if(rating is None):
        rating = ProfessorRatingModel(professorId=professor_id, id=id, createdAt=datetime.now(timezone.utc).isoformat())
    rating.disciplineId = disciplineId
    rating.period = period
    rating.studentId = student_id
    rating.ratings = ratings
    rating.comments = comments
    rating.updatedAt = datetime.now(timezone.utc).isoformat()
    rating.save()
    
    return rating.to_dict()