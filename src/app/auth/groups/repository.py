from src.app.auth.models import GroupPermissionModel
from src.lib.adapters import cognito_adapter

def fetch_groups():
    groups = cognito_adapter.fetch_cognito_groups()
    return groups

def create_group(group):
    group_name = group['id']
    cognito_adapter.create_cognito_group(group_name)
    return True

def delete_group(group_name):
    cognito_adapter.delete_cognito_group(group_name)
    return True

def fetch_group_permissions(group_id):
    items = [e.permissionId for e in GroupPermissionModel.query(groupId=group_id).limit(10000)]
    return items

def update_group_permissions(group_id, permissions_to_add, permissions_to_remove):
    for permission_id in permissions_to_add:
        GroupPermissionModel(groupId=group_id, permissionId=permission_id).save()

    for permission_id in permissions_to_remove:
        GroupPermissionModel.get(groupId=group_id, permissionId=permission_id).delete()
    return True