from flask import request as req
from datetime import datetime, timezone
from src.lib import utils
from src.app.models import ProfessorModel, ProfessorTestimonialModel, ReportedProfessorTestimonialModel

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

def add_testimonial(testimonial):
    testimonial = {k: v for k, v in testimonial.items() if k in 
        ['disciplineId', 'disciplineDepartmentId', 'professorId', 'studentId', 'studentName', 'text', 'anonymous']}
    testimonial['disciplineIdProfessorId'] = f'{testimonial.disciplineId}:{testimonial.professorId}'
    testimonial['createdAt'] = datetime.now(timezone.utc).isoformat()
    testimonial = ProfessorTestimonialModel(**testimonial)
    testimonial.save()
    return testimonial.to_dict()

def update_testimonial(testimonial):
    id = f'{testimonial.disciplineId}:{testimonial.professorId}'
    item = ProfessorTestimonialModel.get(disciplineIdProfessorId=id, createdAt=testimonial.createdAt)
    # Only the own user can update its testimonial
    if(item.studentId != req.user.get('id')):
        raise Exception('Unauthorized')
    item.updatedAt = datetime.now(timezone.utc).isoformat()
    item.text = testimonial.text.strip()
    item.save()
    return item.to_dict()

def remove_testimonial(testimonial):
    id = f'{testimonial.disciplineId}:{testimonial.professorId}'
    item = ProfessorTestimonialModel.get(disciplineIdProfessorId=id, createdAt=testimonial.createdAt)
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