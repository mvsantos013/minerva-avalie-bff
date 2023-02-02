from src.models import TestimonialModel

def fetch_professor_testimonials(professor_id):
    items = [e.to_dict() for e in TestimonialModel.query(professorId=professor_id).limit(10000)]
    return items

def add_testimonial(testimonial):
    testimonial = TestimonialModel(**testimonial)
    testimonial.save()

def update_testimonial(professor_id, student_id, data):
    testimonial = TestimonialModel.get(professorId=professor_id, studentId=student_id)
    testimonial.update(**data)
    testimonial.save()

def remove_testimonial(professor_id, student_id):
    testimonial = TestimonialModel.get(professorId=professor_id, studentId=student_id)
    testimonial.delete()