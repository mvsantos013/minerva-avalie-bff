import json
from decimal import Decimal
from src.lib.logger import Logger
from src.constants import SERVICE_NAME
# Import Mapping, Sequence, Set from dynamodb

logger: Logger = Logger(SERVICE_NAME)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)

def decode_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = decode_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.iterkeys():
            obj[k] = decode_decimals(obj[k])
        return obj
    elif isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def encode_decimals(data):
    """ Sanitizes an object so it can be updated to dynamodb (recursive) """
    if isinstance(data, list):
        for i in range(len(data)):
            data[i] = encode_decimals(data[i])
        return data
    elif isinstance(data, dict):
        for k in data:
            data[k] = encode_decimals(data[k])
        return data
    elif isinstance(data, float):
        return Decimal(str(data))
    else:
        return data

def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')
