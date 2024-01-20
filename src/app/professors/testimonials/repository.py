from flask import request as req
from datetime import datetime, timezone
from src.app.models import ProfessorTestimonialModel, ReportedProfessorTestimonialModel


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