import random
from passlib.hash import pbkdf2_sha256

from workshops_api.authenticators.authenticator import Authenticator
from workshops_api.models.user import UserModel


class KeyAuthenticator(Authenticator):
    """ Authenticates user with pre shared key
    Format: [A-Z0-9]+{length}
    """

    _method = "key"

    def auth(self, credential, is_admin_login):
        if is_admin_login:
            user = UserModel.query.filter_by(full_name='admin').one_or_none()
            if pbkdf2_sha256.verify(credential, user.identity):
                return user
        else:
            return UserModel.query.filter_by(identity=credential).one_or_none()

    def generateKey(self, length=8):
        chars = "0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ"

        return "".join([random.choice(chars) for _ in range(length)])
