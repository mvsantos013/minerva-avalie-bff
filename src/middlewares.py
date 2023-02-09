from flask import jsonify, request as req
from functools import wraps
from src.lib.jwt_verifier import validate_jwt_token

msg = 'Access Denied. Your token may be missing permissions, please login again to generate a new token. Contact a manager if the problem persists.'


def require_permission(required_permissions):
    '''This middleware can be applied to any route to require
    a user to have the specified permission(s).
    '''

    def _require_permission_decorator(f):
        @wraps(f)
        def __require_permission_decorator(*args, **kwargs):
            token = req.headers.get('Authorization')
            user, groups, permissions = validate_jwt_token(token)

            for permission in required_permissions.split('|'):
                if permission in permissions:
                    return f(*args, **kwargs)

            return jsonify({'error': msg}), 403

        return __require_permission_decorator

    return _require_permission_decorator


def require_group(required_groups):
    '''This middleware can be applied to any route to require
    a user to be in the specified group(s).
    '''

    def _require_group_decorator(f):
        @wraps(f)
        def __require_group_decorator(*args, **kwargs):
            token = req.headers.get('Authorization')
            user, groups, permissions = validate_jwt_token(token)

            for group in required_groups.split('|'):
                if group in groups:
                    return f(*args, **kwargs)

            return jsonify({'error': msg}), 403

        return __require_group_decorator

    return _require_group_decorator
