from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV

class PermissionModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-permissions'
        hash_key = 'id'

    class PermissionSchema(Schema):
        id = fields.Str(description='Permission ID')
        description = fields.Str(description='Permission description')

    class Schema(PermissionSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class GroupPermissionModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-groups-permissions'
        hash_key = 'groupId'
        range_key = 'permissionId'

    class GroupPermissionSchema(Schema):
        groupId = fields.Str(description='Group ID')
        permissionId = fields.Str(description='Permission ID')

    class Schema(GroupPermissionSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class AllowedDomainModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-allowed-domains'
        hash_key = 'domain'

    class AllowedDomainSchema(Schema):
        domain = fields.Str(description='Domain')

    class Schema(AllowedDomainSchema):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
