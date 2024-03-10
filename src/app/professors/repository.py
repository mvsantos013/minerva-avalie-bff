import pandas as pd
import json
from uuid import uuid4
from flask import request as req
from src.lib import utils
from datetime import datetime, timezone
from src.app.models import (ProfessorModel, DisciplineProfessorModel, ProfessorTestimonialModel, 
    ProfessorRatingSummaryModel, ReportedProfessorTestimonialModel, DepartmentModel, ProfessorRatingModel)
from src.lib.adapters import s3_adapter
from src.constants import BUCKET_FILES

def fetch_professors():
    professors = [e.to_dict() for e in ProfessorModel.scan().limit(10000)]
    return professors

def fetch_professor(professor_id):
    professor = ProfessorModel.get(id=professor_id)
    return professor.to_dict()

def fetch_professor_disciplines(professor_id):
    professor = ProfessorModel.get(id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')
    disciplines = [e.to_dict() for e in DisciplineProfessorModel.query(professorId=professor_id).limit(10000)]
    return disciplines

def fetch_professor_testimonials(discipline_id, professor_id):
    professor = ProfessorModel.get(id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')
    if(professor.hasPublicTestimonials is False and not utils.user_has_group('Admin')): # Hide testimonials if it's not public
        return []
    testimonials = []
    user_id = req.user.get('id') if req.user else None 

    for testimonial in ProfessorTestimonialModel.query(disciplineIdProfessorId=f'{discipline_id}:{professor_id}').limit(10000):
        testimonial = testimonial.to_dict()
        if(testimonial.get('anonymous') is True):
            testimonial['studentName'] = 'Anônimo'
            if(testimonial['studentId'] != user_id): # Hide ids that are not the user's
                testimonial['studentId'] = None
        testimonials.append(testimonial)
        
    return testimonials

def add_professor(professor):
    professor['id'] = str(uuid4())
    picture = professor.get('picture')
    del professor['picture']

    # Upload picture to S3
    if picture:
        picture_extension = picture.filename.split('.')[-1]
        s3_path = f'public/imgs/professors/prof-{professor["id"]}.{picture_extension}'
        s3_adapter.upload_file(s3_path, picture)
        professor['pictureUrl'] = f'https://{BUCKET_FILES}.s3.amazonaws.com/{s3_path}'

    del professor['disciplinesToAdd']
    del professor['disciplinesToRemove']

    professor = ProfessorModel(**professor)
    professor.save()

def add_professors_from_csv(file):
    df = pd.read_csv(file, sep=',')
    if(sorted(df.columns) != sorted(['departmentId', 'name', 'description', 'about', 'hasPublicRating', 'hasPublicTestimonials', 'hasPublicStatistics'])):
        raise Exception('Invalid CSV file.')
    departments = [e.id for e in DepartmentModel.scan().limit(10000)]
    if(not all([e in departments for e in df.departmentId.unique()])):
        deps = [e for e in df.departmentId.unique() if e not in departments]
        raise Exception(f'Departamento(s) inexistente(s): {deps}.')

    df['id'] = [str(uuid4()) for _ in range(len(df))]

    rows = df.to_dict('records')
    ProfessorModel.put_batch(*rows)

def update_professor(professor_id, data):
    data['id'] = professor_id
    professor = ProfessorModel.get(id=professor_id)
    
    # Update picture
    picture = data.get('picture')
    del data['picture']
    if picture:
        picture_extension = picture.filename.split('.')[-1]
        s3_path = f'public/imgs/professors/prof-{professor_id}.{picture_extension}'
        s3_adapter.upload_file(s3_path, picture)
        data['pictureUrl'] = f'https://{BUCKET_FILES}.s3.amazonaws.com/{s3_path}'

    disciplines_to_add = json.loads(data.get('disciplinesToAdd', '[]'))
    disciplines_to_remove = json.loads(data.get('disciplinesToRemove', '[]'))
    del data['disciplinesToAdd']
    del data['disciplinesToRemove']

    professor.update(**data)
    professor.save()

    if(len(disciplines_to_add) > 0):
        DisciplineProfessorModel.put_batch(*disciplines_to_add)
    for pd in disciplines_to_remove:
        DisciplineProfessorModel.Table.delete_item(**pd)

def remove_professor(professor_id):
    professor = ProfessorModel.get(id=professor_id)

    # Delete picture from S3
    if getattr(professor, 'pictureUrl', None):
        s3_path = professor.pictureUrl.split(f'{BUCKET_FILES}.s3.amazonaws.com/')[1]
        if(s3_adapter.file_exists(s3_path)):
            s3_adapter.delete_file(s3_path)

    professor.delete()

def fetch_discipline_professors_ratings_summary(department_id, discipline_id):
    id = f"{department_id}:{discipline_id}"
    discipline_professors_ids = [{'id': e.professorId} for e in DisciplineProfessorModel.ByDiscipline.query(departmentIdDisciplineId=id).limit(1000)]
    
    # Get professors with public ratings
    professors = ProfessorModel.get_batch(keys=discipline_professors_ids, attrs='id,hasPublicRating')
    professors_public_ratings = {e.id: e.hasPublicRating for e in professors}
    
    # Get professors that the student has rated
    student_id = req.user['id']
    student_ratings = ProfessorRatingModel.ByStudent.query(studentId=student_id).limit(10000)
    student_professors_rated = {e.disciplineId + e.professorId: True for e in student_ratings }

    ratings_summary = ProfessorRatingSummaryModel.ByDiscipline.query(disciplineId=discipline_id).limit(10000)
    result = []
    for rs in ratings_summary:
        has_public_rating = professors_public_ratings.get(rs.professorId, False)
        student_has_rated = student_professors_rated.get(rs.disciplineId + rs.professorId, False)
        item = rs.to_dict()
        if(has_public_rating):
            item['studentHasRated'] = True
            if(not student_has_rated):
                del item['averageValue']
                del item['count']
                del item['details']
                item['studentHasRated'] = True # False
            result.append(item)
    return result


def remove_testimonial(testimonial):
    id = f"{testimonial['disciplineId']}:{testimonial['professorId']}"
    item = ProfessorTestimonialModel.get(disciplineIdProfessorId=id, studentId=testimonial['studentId'])
    # Only the own user can remove its testimonial
    if(item.studentId != req.user.get('id')):
        raise Exception('Unauthorized')
    testimonial.delete()

def report_testimonial(testimonial):
    testimonial['reportedAt'] = datetime.now(timezone.utc).isoformat()
    testimonial = ReportedProfessorTestimonialModel(**testimonial)
    testimonial.save()
    return testimonial.to_dict()

def fetch_reported_testimonials():
    testimonials = []
    for testimonial in ReportedProfessorTestimonialModel.scan().limit(10000):
        testimonial = testimonial.to_dict()
        if(testimonial.get('anonymous') is True):
            testimonial['studentName'] = 'Anônimo'
            testimonial['studentId'] = None
        testimonials.append(testimonial)
    return testimonials

def approve_reported_testimonial(testimonial):
    testimonial = ReportedProfessorTestimonialModel.get(disciplineIdProfessorId=testimonial.disciplineIdProfessorId, createdAt=testimonial.createdAt)
    testimonial.delete()

def remove_reported_testimonial(testimonial):
    reported_testimonial = ReportedProfessorTestimonialModel.get(disciplineIdProfessorId=testimonial.disciplineIdProfessorId, createdAt=testimonial.createdAt)
    reported_testimonial.delete()
    testimonial = ProfessorTestimonialModel.get(disciplineIdProfessorId=testimonial.disciplineIdProfessorId, createdAt=testimonial.createdAt)
    testimonial.delete()