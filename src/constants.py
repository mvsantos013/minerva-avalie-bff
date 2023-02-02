import os

ENV: str = os.environ.get('STAGE', 'dev')
SERVICE_NAME: str = os.environ.get('SERVICE_NAME', 'minerva-avalie-bff')
AWS_ACCOUNT_ID: str = os.environ.get('AWS_ACCOUNT_ID', '670419627080')
AWS_REGION: str = 'us-east-1'
IS_LOCAL: bool = os.environ.get("AWS_EXECUTION_ENV") is None
IS_DEV: bool = not IS_LOCAL and ENV == 'dev'
IS_PROD: bool = ENV == 'prod'