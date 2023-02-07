import boto3
from src.constants import COGNITO_USER_POOL_ID

cognito = None

def get_cognito_client():
    global cognito
    if cognito is None:
        cognito = boto3.client('cognito-idp')
    return cognito

def fetch_cognito_groups():
    response = get_cognito_client().list_groups(
        UserPoolId=COGNITO_USER_POOL_ID,
        Limit=60
    )
    groups = [{'id': g['GroupName']} for g in response['Groups']]
    return groups

def create_cognito_group(group_name):
    get_cognito_client().create_group(
        UserPoolId=COGNITO_USER_POOL_ID,
        GroupName=group_name,
    )
    return True

def delete_cognito_group(group_name):
    get_cognito_client().delete_group(
        UserPoolId=COGNITO_USER_POOL_ID,
        GroupName=group_name,
    )
    return True