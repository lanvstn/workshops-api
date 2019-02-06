from flask_restful import Resource, reqparse, abort
from flask import request
import re
from passlib.hash import pbkdf2_sha256

from workshops_api import auth
from workshops_api.database import db
from workshops_api.app import app


class AuthConfigResource(Resource):
    def get(self):
        # Currently unused, but would be used to query for the configured auth method of API
        return {
            "method": auth.authenticator._method
        }


class AuthLoginResource(Resource):
    def get(self):
        user = auth.verify_request(request)

        if not user:
            abort(401)

        return {
            "id": user.id,
            "full_name": user.full_name,
            "permission": user.permission,
            "targetGroup": user.targetGroup,
            "event_id": user.event_id
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('credential')
        parser.add_argument('admin_login')
        args = parser.parse_args()

        credential = args['credential']
        admin_login = args['admin_login']

        if (credential is None) or (admin_login is None):
            abort(400)

        if admin_login == '0':
            is_admin_login = False
        else:
            is_admin_login = True

        user = auth.verify_credential(credential, is_admin_login)
        if user == '':
            abort(401)

        return {
            "token": auth.create_token(credential, is_admin_login)
        }


class AuthAdminPasswordChangeResource(Resource):
    # Assumes usage of KeyAuthenticator, needs to be changed if others are added

    @auth.required('manage')
    def post(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('old_password')
        parser.add_argument('new_password')
        args = parser.parse_args()

        old_password = args['old_password']
        new_password = args['new_password']

        if (not old_password) or (not new_password):
            abort(
                400,
                description="No data"
            )

        # Requirements check: 1 uppercase, 1 lowercase, 1 number, length 10+
        requirements = [re.compile(r"[A-Z]+"), re.compile(r"[a-z]+"), re.compile(r"[0-9]+")]
        for regex in requirements:
            if re.search(regex, new_password) is None:
                abort(
                    400,
                    description="Password did not meet requirements"
                )

        if len(new_password) < 10:
            abort(
                400,
                description="Password too short, needs to be at least 10 characters"
            )

        # Old password check
        admin_user = auth.verify_credential(old_password, True)

        if admin_user is None:
            abort(
                400,
                description="Bad old password"
            )

        # OK, change password
        admin_user.identity = pbkdf2_sha256.hash(new_password)
        db.session.merge(admin_user)
        db.session.commit()

        app.logger.info(
            f"{admin_user.id}:{admin_user.full_name} ({request.remote_addr}) "
            f"changed admin password"
        )

        # User should replace their token with this one now
        return {
            "token": auth.create_token(new_password, True)
        }
