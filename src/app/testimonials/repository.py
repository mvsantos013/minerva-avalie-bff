from uuid import uuid4
from datetime import datetime, timezone
from src.lib import utils
from src.models import ProfessorModel, TestimonialModel

def fetch_professor_testimonials(department_id, professor_id):
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')
    if(professor.publicTestimonials is False and not utils.user_has_group('Admin')): # Hide testimonials if it's not public
        return []
    items = [e.to_dict() for e in TestimonialModel.query(professorId=professor_id).limit(10000)]
    return items

def add_testimonial(testimonial):
    testimonial = {k: v for k, v in testimonial.items() if k in ['professorId', 'studentId', 'studentName', 'text']}
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