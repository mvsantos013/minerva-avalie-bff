from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV


class ProfessorRatingModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-professors-ratings'
        hash_key = 'professorId'
        range_key = 'createdAt'

    class ProfessorRatingSchema(Schema):
        professorId = fields.Str(description='Professor ID')
        disciplineId = fields.Str(description='Discipline ID')
        period = fields.Str(description='Period when the discipline was taken')
        studentId = fields.Str(description='Student ID')
        ratings = fields.Dict(description='Rating', keys=fields.Str(), values=fields.Decimal())
        comments = fields.Dict(description='Comments', keys=fields.Str(), values=fields.Str(), allow_none=True, default={})
        createdAt = fields.Str(description='Post date')
        updatedAt = fields.Str(description='Update date')

    class Schema(ProfessorRatingSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)