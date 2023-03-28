from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV


class DisciplineModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-disciplines'
        hash_key = 'organizationId'
        range_key = 'id'

    class DisciplineSchema(Schema):
        organizationId = fields.Str(description='Organization ID')
        id = fields.Str(description='Discipline ID')
        name = fields.Str(description='Discipline name')

    class Schema(DisciplineSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
