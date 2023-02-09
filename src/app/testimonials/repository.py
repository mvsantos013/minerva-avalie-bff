from uuid import uuid4
from datetime import datetime, timezone
from src.models import TestimonialModel

def fetch_professor_testimonials(professor_id):
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