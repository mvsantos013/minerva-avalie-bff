import boto3
from datetime import datetime, timezone
from src.constants import COGNITO_USER_POOL_ID

'''
    This lambda function executes after a user is registered.
    It adds the user to the default group.
'''

STUDENT_GROUP = 'Student'

cognito = boto3.client('cognito-idp')

def handler(event, context):
    email = event['request']['userAttributes']['email']
    cognito.admin_add_user_to_group(
        UserPoolId=COGNITO_USER_POOL_ID, 
        Username=email, 
        GroupName=STUDENT_GROUP
    )
    return event
