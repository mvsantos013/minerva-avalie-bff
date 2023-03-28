import json
from src.app.auth.models import GroupPermissionModel


'''
    This lambda function executes when the user login.
    It checks for the user permissions and add to the JWT token.
'''


def handler(event, context):
    user_groups = event['request']['groupConfiguration']['groupsToOverride']
    
    # Ignore Google group
    user_groups = [g for g in user_groups if 'Google' not in g]

    permissions = []
    for group_id in user_groups:
        group_permissions = GroupPermissionModel.query(groupId=group_id)
        for permission in group_permissions:
            permissions.append(permission.permissionId)

    # Add info to the JWT token
    event['response']['claimsOverrideDetails'] = {
        'claimsToAddOrOverride': {
            'userData': json.dumps({
                'groups': user_groups,
                'permissions': permissions,
            })
        }
    }

    return event
