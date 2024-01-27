from uuid import uuid4
from flask import request as req
from src.lib import utils
from datetime import datetime, timezone
from src.app.models import (ProfessorModel, DisciplineProfessorModel, ProfessorTestimonialModel, 
    ProfessorRatingSummaryModel, ReportedProfessorTestimonialModel)
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

    professor = ProfessorModel(**professor)
    professor.save()

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

    professor.update(**data)
    professor.save()

def remove_professor(professor_id):
    professor = ProfessorModel.get(id=professor_id)

    # Delete picture from S3
    if getattr(professor, 'pictureUrl', None):
        s3_path = professor.pictureUrl.split(f'{BUCKET_FILES}.s3.amazonaws.com/')[1]
        if(s3_adapter.file_exists(s3_path)):
            s3_adapter.delete_file(s3_path)

    professor.delete()

def fetch_professor_ratings_of_discipline(discipline_id):
    items = [e.to_dict() for e in ProfessorRatingSummaryModel.ByDiscipline.query(disciplineId=discipline_id).limit(10000)]
    return items


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