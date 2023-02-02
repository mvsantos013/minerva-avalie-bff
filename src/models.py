from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV

class ProfessorModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors'
        hash_key = 'departmentId'
        range_key = 'id'

    class ProfessorSchema(Schema):
        id = fields.Str(description='Professor ID')
        departmentId = fields.Str(description='Department ID')
        name = fields.Str(description='Professor name')
        description = fields.Str(description='Professor description')
        about = fields.Str(description='Professor extended description')
        pictureUrl = fields.Str(description='S3 URI picture', allow_none=True)

    class Schema(ProfessorSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class TestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-testimonials'
        hash_key = 'professorId'
        range_key = 'studentId'

    class TestimonialSchema(Schema):
        professorId = fields.Str(description='Professor ID')
        studentId = fields.Str(description='Student ID')
        text = fields.Str(description='Content')
        postedAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date')

    class Schema(TestimonialSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)