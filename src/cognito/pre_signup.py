from src.models import AllowedDomainModel

'''
    This lambda function executes when the user is about to be registered.
    It checks if the email domain is allowed.
'''


def handler(event, context):
    allowed_domains = [e.to_dict()['domain'] for e in AllowedDomainModel.scan().limit(10000)]

    email = event['request']['userAttributes']['email']

    domain = email.split('@')[1]

    if domain not in allowed_domains:
        raise Exception('Invalid email domain.')

    return event