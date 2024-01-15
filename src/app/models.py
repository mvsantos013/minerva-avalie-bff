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
        hasPpublicProfessorTestimonials = fields.Bool(description='ProfessorTestimonials are public', default=False)
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

class ProfessorTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-testimonials'
        hash_key = 'disciplineIdProfessorId'
        range_key = 'createdAt'

    class ProfessorTestimonialSchema(Schema):
        disciplineIdProfessorId = fields.Str(description='Discipline ID and Professor ID')
        professorId = fields.Str(description='Professor ID')
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        createdAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date')

    class Schema(ProfessorTestimonialSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ReportedProfessorTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-reported-testimonials'
        hash_key = 'disciplineIdProfessorId'
        range_key = 'createdAt'

    class ReportedProfessorTestimonialModel(Schema):
        disciplineIdProfessorId = fields.Str(description='Discipline ID and Professor ID')
        professorId = fields.Str(description='Professor ID')
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        createdAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date')

    class Schema(ReportedProfessorTestimonialModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class DisciplineTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-testimonials'
        hash_key = 'departmentIdDisciplineId'
        range_key = 'createdAt'

    class DisciplineTestimonialSchema(Schema):
        departmentIdDisciplineId = fields.Str(description='Department ID and Discipline ID')
        professorId = fields.Str(description='Professor ID')
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        createdAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date')

    class Schema(DisciplineTestimonialSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ReportedDisciplineTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-reported-testimonials'
        hash_key = 'departmentIdDisciplineId'
        range_key = 'createdAt'

    class ReportedDisciplineTestimonialModel(Schema):
        departmentIdDisciplineId = fields.Str(description='Department ID and Discipline ID')
        professorId = fields.Str(description='Professor ID')
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        createdAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date')

    class Schema(ReportedDisciplineTestimonialModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class DisciplineQuestionModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-questions'
        hash_key = 'id'

    class DisciplineQuestionSchema(Schema):
        id = fields.Str(description='ID')
        question = fields.Str(description='Question')
        type = fields.Str(description='Type')
        active = fields.Bool(description='Active', default=False)

    class Schema(DisciplineQuestionSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class QuestionModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-questions'
        hash_key = 'id'

    class QuestionSchema(Schema):
        id = fields.Str(description='ID')
        question = fields.Str(description='Question')
        type = fields.Str(description='Type')
        questionType = fields.Str(description='Question format')
        active = fields.Bool(description='Active', default=False)

    class Schema(QuestionSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
