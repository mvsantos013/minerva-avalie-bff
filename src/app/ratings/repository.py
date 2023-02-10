from datetime import datetime, timezone
from src.lib import utils
from src.models import ProfessorModel, ProfessorRatingModel

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
    ratings = ProfessorRatingModel.get(professorId=professor_id, studentId=student_id)
    if(ratings is None):
        return {}
    return ratings.to_dict()

def rate_professor(department_id, professor_id, student_id, ratings, comments):
    if('total' in ratings):
        del ratings['total']

    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)

    if(professor is None):
        raise Exception('Professor not found')

    rating = ProfessorRatingModel.get(professorId=professor_id, studentId=student_id)
    
    # If professor has no rating summary, create one with zero values
    if(not getattr(professor, 'ratingSummary', None)):
        professor.ratingSummary = {'total': 0}
        for key in ratings:
            professor.ratingSummary[key] = 0

    # User is rating for the first time
    if(rating is None):
        rating = ProfessorRatingModel(professorId=professor_id, studentId=student_id)
        rating.postedAt = datetime.now(timezone.utc).isoformat()
        # Update professor rating summary
        professor.ratingSummary['total'] += 1
        total = professor.ratingSummary['total']
        for key in ratings:
            professor.ratingSummary[key] = ((professor.ratingSummary[key] * (total - 1)) + ratings[key]) / total

    else: # User is updating his rating
        rating.updatedAt = datetime.now(timezone.utc).isoformat()

        # Update professor rating summary
        total = professor.ratingSummary['total']
        for key in ratings:
            current_rating = rating.ratings[key] if key in rating.ratings else 0
            professor.ratingSummary[key] = ((professor.ratingSummary[key] * total) - current_rating + ratings[key]) / total

    # Save student individual rating
    rating.ratings = ratings
    rating.comments = comments
    rating.save()

    professor.ratingSummary = utils.encode_decimals(professor.ratingSummary)
    professor.save()
    return True