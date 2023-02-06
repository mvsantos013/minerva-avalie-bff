import os

ENV: str = os.environ.get('STAGE', 'dev')
SERVICE_NAME: str = os.environ.get('SERVICE_NAME', 'minerva-avalie-bff')
AWS_ACCOUNT_ID: str = os.environ.get('AWS_ACCOUNT_ID', '670419627080')
AWS_REGION: str = 'us-east-1'
IS_LOCAL: bool = os.environ.get("AWS_EXECUTION_ENV") is None
IS_DEV: bool = not IS_LOCAL and ENV == 'dev'
IS_PROD: bool = ENV == 'prod'

BUCKET_FILES: str = f'{SERVICE_NAME}-files-{ENV}' 

COGNITO_USER_POOL_ID: str = '#' if ENV == 'prod' else 'us-east-1_kR9WTqcBB'
COGNITO_APP_CLIENT_ID: str = '#' if ENV == 'prod' else '2ukub13155vbklac47l88gt0qm'