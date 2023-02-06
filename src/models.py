from dynamorm import DynaModel
from marshmallow import Schema, fields
from src.constants import SERVICE_NAME, ENV

class PermissionModel(DynaModel):
    class Table:
        name = f'{SERVICE_NAME}-{ENV}-permissions'
        hash_key = 'id'

    class PermissionSchema(Schema):
        id = fields.Str(description='Permission ID')

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
        publicRating = fields.Bool(description='Public rating', default=False)

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