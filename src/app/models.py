from dynamorm import DynaModel, GlobalIndex, ProjectAll
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV


class ConfigurationModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-configurations'
        hash_key = 'name'

    class ConfigurationSchema(Schema):
        name = fields.Str(description='Parameter name')
        value = fields.Str(description='Parameter Value')

    class Schema(ConfigurationSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


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
        description = fields.Str(description='Discipline description', allow_none=True, default='')

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
        hasPublicTestimonials = fields.Bool(description='ProfessorTestimonials are public', default=False)
        hasPublicStatistics = fields.Bool(description='Statistics are public', default=False)


    class Schema(ProfessorSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class DisciplineProfessorModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-professors'
        hash_key = 'professorId'
        range_key = 'departmentIdDisciplineId'

    class ByDiscipline(GlobalIndex):
        name = 'gsiDisciplineId'
        hash_key = 'departmentIdDisciplineId'
        range_key = 'professorId'
        projection = ProjectAll()

    class DisciplineProfessorSchema(Schema):
        professorId = fields.Str(description='Professor ID')
        departmentIdDisciplineId = fields.Str(description='Department ID : Discipline ID')

    class Schema(DisciplineProfessorSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class ProfessorTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-testimonials'
        hash_key = 'disciplineIdProfessorId'
        range_key = 'studentId'

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

    class Schema(ProfessorTestimonialSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ReportedProfessorTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-reported-testimonials'
        hash_key = 'disciplineIdProfessorId'
        range_key = 'studentId'

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
        reportedAt = fields.Str(description='Report date')

    class Schema(ReportedProfessorTestimonialModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class DisciplineTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-testimonials'
        hash_key = 'disciplineId'
        range_key = 'professorIdStudentId'

    class DisciplineTestimonialSchema(Schema):
        disciplineId = fields.Str(description='Discipline ID')
        professorIdStudentId = fields.Str(description='Professor ID : Student ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        professorId = fields.Str(description='Professor ID')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        createdAt = fields.Str(description='Post date')

    class Schema(DisciplineTestimonialSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ReportedDisciplineTestimonialModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-reported-testimonials'
        hash_key = 'disciplineId'
        range_key = 'professorIdStudentId'

    class ReportedDisciplineTestimonialModel(Schema):
        disciplineId = fields.Str(description='Discipline ID')
        professorIdStudentId = fields.Str(description='Professor ID : Student ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        professorId = fields.Str(description='Professor ID')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        text = fields.Str(description='Content')
        anonymous = fields.Bool(description='Anonymous', default=False)
        createdAt = fields.Str(description='Post date')
        reportedAt = fields.Str(description='Report date')

    class Schema(ReportedDisciplineTestimonialModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class QuestionModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-questions'
        hash_key = 'id'

    class QuestionSchema(Schema):
        id = fields.Str(description='ID')
        title = fields.Str(description='Question')
        description = fields.Str(description='Question')
        type = fields.Str(description='Type')
        questionType = fields.Str(description='Question format')
        active = fields.Bool(description='Active', default=False)
        order = fields.Int(description='Order', default=0)

    class Schema(QuestionSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class DisciplineRatingModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-ratings'
        hash_key = 'disciplineIdProfessorIdPeriod'
        range_key = 'studentId'

    class DisciplineRatingModel(Schema):
        disciplineIdProfessorIdPeriod = fields.Str(description='Discipline ID : Professor ID : Period')
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        professorId = fields.Str(description='Professor ID')
        period = fields.Str(description='Period')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        ratings = fields.Dict(description='Ratings')
        createdAt = fields.Str(description='Post date')

    class Schema(DisciplineRatingModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class ProfessorRatingModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-ratings'
        hash_key = 'disciplineIdProfessorIdPeriod'
        range_key = 'studentId'

    class ByStudent(GlobalIndex):
        name = 'gsiStudentId'
        hash_key = 'studentId'
        range_key = 'disciplineIdProfessorIdPeriod'
        projection = ProjectAll()

    class ProfessorRatingModel(Schema):
        disciplineIdProfessorIdPeriod = fields.Str(description='Discipline ID : Professor ID : Period')
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        professorId = fields.Str(description='Professor ID')
        period = fields.Str(description='Period')
        studentId = fields.Str(description='Student ID')
        studentName = fields.Str(description='Student name')
        ratings = fields.Dict(description='Ratings')
        createdAt = fields.Str(description='Post date')

    class Schema(ProfessorRatingModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class DisciplineRatingSummaryModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines-ratings-summary'
        hash_key = 'disciplineId'
        range_key = 'professorId'

    class ByProfessor(GlobalIndex):
        name = 'gsiProfessorId'
        hash_key = 'professorId'
        range_key = 'disciplineId'
        projection = ProjectAll()
    class DisciplineRatingSummaryModel(Schema):
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        professorId = fields.Str(description='Professor ID')
        details = fields.List(fields.Dict(description='Ratings details'))
        averageValue = fields.Decimal(description='Average value')
        count = fields.Int(description='Count')
        createdAt = fields.Str(description='Post date')

    class Schema(DisciplineRatingSummaryModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class ProfessorRatingSummaryModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-ratings-summary'
        hash_key = 'professorId'
        range_key = 'disciplineId'
    
    class ByDiscipline(GlobalIndex):
        name = 'gsiDisciplineId'
        hash_key = 'disciplineId'
        range_key = 'professorId'
        projection = ProjectAll()

    class ProfessorRatingSummaryModel(Schema):
        disciplineId = fields.Str(description='Discipline ID')
        disciplineDepartmentId = fields.Str(description='Discipline department ID')
        professorId = fields.Str(description='Professor ID')
        details = fields.List(fields.Dict(description='Ratings details'))
        averageValue = fields.Decimal(description='Average value')
        count = fields.Int(description='Count')
        createdAt = fields.Str(description='Post date')

    class Schema(ProfessorRatingSummaryModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)