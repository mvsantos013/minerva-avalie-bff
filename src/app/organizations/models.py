from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV


class OrganizationModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-organizations'
        hash_key = 'id'

    class OrganizationSchema(Schema):
        organizationId = fields.Str(description='Organization ID')
        id = fields.Str(description='Organization ID')
        name = fields.Str(description='Organization name')

    class Schema(OrganizationSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
