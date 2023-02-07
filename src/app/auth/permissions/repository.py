from uuid import uuid4
from src.models import PermissionModel


def fetch_permissions():
    items = [e.to_dict() for e in PermissionModel.scan().limit(10000)]
    return items

def create_permission(permission):
    permission = PermissionModel(**permission)
    permission.save()

def delete_permission(permission_id):
    permission = PermissionModel.get(id=permission_id)
    permission.delete()