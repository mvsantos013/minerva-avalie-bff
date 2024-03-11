import boto3
from src.constants import COGNITO_USER_POOL_ID

'''
    This lambda function executes after a user is registered.
    It adds the user to the default group.
'''

INITIAL_GROUP = 'Student'

cognito = boto3.client('cognito-idp')

def handler(event, context):
    cognito.admin_add_user_to_group(
        UserPoolId=COGNITO_USER_POOL_ID, 
        Username=event['userName'], 
        GroupName=INITIAL_GROUP
    )
    return event