from flask import request as req
from uuid import uuid4
from datetime import datetime, timezone
from src.lib import utils
from src.app.professors.models import ProfessorModel
from src.app.professors.testimonials.models import TestimonialModel, ReportedTestimonialModel

def fetch_professor_testimonials(department_id, professor_id):
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')
    if(professor.publicTestimonials is False and not utils.user_has_group('Admin')): # Hide testimonials if it's not public
        return []
    testimonials = []
    user_id = req.user.get('id') if req.user else None 

    for testimonial in TestimonialModel.query(professorId=professor_id).limit(10000):
        testimonial = testimonial.to_dict()
        if('anonymous' in testimonial and testimonial['anonymous'] is True):
            testimonial['studentName'] = 'Anônimo'
            if(testimonial['studentId'] != user_id):
                testimonial['studentId'] = None
        testimonials.append(testimonial)
        
    return testimonials

def add_testimonial(testimonial):
    testimonial = {k: v for k, v in testimonial.items() if k in ['professorId', 'studentId', 'studentName', 'text', 'anonymous']}
    testimonial['id'] = str(uuid4())
    testimonial['postedAt'] = datetime.now(timezone.utc).isoformat()
    testimonial = TestimonialModel(**testimonial)
    testimonial.save()
    return testimonial.to_dict()

def update_testimonial(professor_id, testimonial_id, text):
    testimonial = TestimonialModel.get(professorId=professor_id, id=testimonial_id)
    testimonial.updatedAt = datetime.now(timezone.utc).isoformat()
    testimonial.text = text
    testimonial.save()
    return testimonial.to_dict()

def remove_testimonial(professor_id, testimonial_id):
    testimonial = TestimonialModel.get(professorId=professor_id, id=testimonial_id)
    testimonial.delete()

def report_testimonial(testimonial):
    testimonial['reportedAt'] = datetime.now(timezone.utc).isoformat()
    testimonial = ReportedTestimonialModel(**testimonial)
    testimonial.save()
    return testimonial.to_dict()

def fetch_reported_testimonials():
    testimonials = []
    for testimonial in ReportedTestimonialModel.scan().limit(10000):
        testimonial = testimonial.to_dict()
        if('anonymous' in testimonial and testimonial['anonymous'] is True):
            testimonial['studentName'] = 'Anônimo'
            testimonial['studentId'] = None
        testimonials.append(testimonial)
    return testimonials

def approve_reported_testimonial(professor_id, testimonial_id):
    testimonial = ReportedTestimonialModel.get(professorId=professor_id, id=testimonial_id)
    testimonial.delete()

def remove_reported_testimonial(professor_id, testimonial_id):
    reported_testimonial = ReportedTestimonialModel.get(professorId=professor_id, id=testimonial_id)
    reported_testimonial.delete()
    testimonial = TestimonialModel.get(professorId=professor_id, id=testimonial_id)
    testimonial.delete()