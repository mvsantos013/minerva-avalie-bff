from dynamorm import DynaModel, GlobalIndex, ProjectAll
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV


class DepartmentModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-departments'
        hash_key = 'id'

    class DepartmentSchema(Schema):
        id = fields.Str(description='Department ID')
        name = fields.Str(description='Department name')

    class Schema(DepartmentSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class DisciplineModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines'
        hash_key = 'departmentId'
        range_key = 'id'

    class DisciplineSchema(Schema):
        departmentId = fields.Str(description='DepartmentId ID')
        id = fields.Str(description='Discipline ID')
        name = fields.Str(description='Discipline name')

    class Schema(DisciplineSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ProfessorModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors'
        hash_key = 'id'

    class ProfessorSchema(Schema):
        id = fields.Str(description='Professor ID')
        departmentId = fields.Str(description='Department ID of the professor')
        name = fields.Str(description='Professor name')
        description = fields.Str(description='Professor description', allow_none=True, default='')
        about = fields.Str(description='Professor extended description', allow_none=True, default='')
        pictureUrl = fields.Str(description='S3 URI picture', allow_none=True, default='')
        hasPublicRating = fields.Bool(description='Ratings are public', default=False)
        hasPpublicTestimonials = fields.Bool(description='Testimonials are public', default=False)
        hasPpublicStatistics = fields.Bool(description='Statistics are public', default=False)


    class Schema(ProfessorSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class DisciplineProfessorModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professor-disciplines'
        hash_key = 'professorId'
        range_key = 'disciplineId'

    class ByDiscipline(GlobalIndex):
        name = 'gsiDisciplineId'
        hash_key = 'disciplineId'
        range_key = 'professorId'
        projection = ProjectAll()

    class DisciplineProfessorSchema(Schema):
        professorId = fields.Str(description='Professor ID')
        disciplineId = fields.Str(description='Discipline ID')

    class Schema(DisciplineProfessorSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
