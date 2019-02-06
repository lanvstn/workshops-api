from functools import wraps
from flask import request
from flask_restful import abort
import jwt
from datetime import datetime, timedelta

from workshops_api.authenticators.key import KeyAuthenticator
from workshops_api.config import config


ACCESS_LEVELS = {
    'none': 0,
    'user': 1,
    'manage': 10,
    'admin': 100
}

authenticator = KeyAuthenticator()


def required(access_level):
    """ Method decorator for authentication """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            user = verify_request(request)
            _401_if_no_user(user)
            if user.permission < ACCESS_LEVELS[access_level]:
                abort(401)

            kwargs['auth_user'] = user

            return f(*args, **kwargs)
        return wrapper
    return decorator


def restrict_to_self():
    """ Method decorator for authentication """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            user = verify_request(request)
            _401_if_no_user(user)
            if user.permission >= ACCESS_LEVELS['manage'] or user.id != int(kwargs['user_id']):
                # Privileged user is permitted to access other users data
                # Normal user can access his own data
                abort(401)

            return f(*args, **kwargs)
        return wrapper
    return decorator


def create_token(credential, is_admin_login):
    """ Returns a JWT to send to the user """

    user = authenticator.auth(credential, is_admin_login)

    _401_if_no_user(user)

    if not is_admin_login:
        admin_login = 0
    else:
        admin_login = 1

    payload = {
        "exp": datetime.utcnow() + timedelta(days=365),
        "credential": credential,
        "admin_login": admin_login
    }

    token = jwt.encode(payload, config.config['app']['jwt_secret'], algorithm="HS256")

    # Need ASCII representation or Python will write b'token' in the headers
    return token.decode('ascii')


def verify_request(request):
    """ Decodes JWT in headers and returns user with credentials if match """

    auth_header = request.headers.get("Authorization")

    if auth_header:
        auth_token = auth_header.split(" ")[1]
        decoded_JWT = jwt.decode(auth_token, config.config['app']['jwt_secret'])

        credential = decoded_JWT["credential"]

        if decoded_JWT["admin_login"] == 0:
            is_admin_login = False
        else:
            is_admin_login = True

        return authenticator.auth(credential, is_admin_login)
    else:
        return ''


def verify_credential(credential, is_admin_login):
    """ Only verify credential. Used during login """

    return authenticator.auth(credential, is_admin_login=is_admin_login)


def _401_if_no_user(user):
    if not user:
        abort(401)
