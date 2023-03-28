from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV


class DepartmentModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-departments'
        hash_key = 'organizationId'
        range_key = 'id'

    class DepartmentSchema(Schema):
        organizationId = fields.Str(description='Organization ID')
        id = fields.Str(description='Department ID')
        name = fields.Str(description='Department name')

    class Schema(DepartmentSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
