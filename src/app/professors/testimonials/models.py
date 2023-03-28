from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV


class TestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-testimonials'
        hash_key = 'professorId'
        range_key = 'id'

    class TestimonialSchema(Schema):
        professorId = fields.Str(description='Professor ID')
        id = fields.Str(description='Testimonial ID')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        postedAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date')

    class Schema(TestimonialSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ReportedTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-reported-testimonials'
        hash_key = 'professorId'
        range_key = 'id'

    class ReportedTestimonialModel(Schema):
        departmentId = fields.Str(description='Department ID')
        professorId = fields.Str(description='Professor ID')
        id = fields.Str(description='Testimonial ID')
        studentId = fields.Str(description='Student ID', allow_none=True, default=None)
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        postedAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date', default=None, allow_none=True)
        reportedAt = fields.Str(description='Report date')

    class Schema(ReportedTestimonialModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
