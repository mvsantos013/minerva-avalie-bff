from dynamorm import DynaModel, GlobalIndex, ProjectAll
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
        description = fields.Str(description='Professor description', allow_none=True, default='')
        about = fields.Str(description='Professor extended description', allow_none=True, default='')
        pictureUrl = fields.Str(description='S3 URI picture', allow_none=True, default='')
        ratingSummary = fields.Dict(description='Rating summary', allow_none=True, default={})
        publicRating = fields.Bool(description='Public rating', default=False)
        publicTestimonials = fields.Bool(description='Public testimonials', default=False)
        publicStatistics = fields.Bool(description='Public statistics', default=False)


    class Schema(ProfessorSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class ProfessorDisciplineModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-disciplines'
        hash_key = 'professorId'
        range_key = 'disciplineId'

    class ByDiscipline(GlobalIndex):
        name = 'gsiDisciplineId'
        hash_key = 'disciplineId'
        range_key = 'professorId'
        projection = ProjectAll()

    class ProfessorDisciplineSchema(Schema):
        professorId = fields.Str(description='Professor ID')
        disciplineId = fields.Str(description='Discipline ID')

    class Schema(ProfessorDisciplineSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
