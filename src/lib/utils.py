from src.lib.logger import Logger
from src.constants import SERVICE_NAME

logger: Logger = Logger(SERVICE_NAME)


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')
