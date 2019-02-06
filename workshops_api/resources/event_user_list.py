from flask_restful import Resource, abort
from flask import request
import sqlalchemy.exc

from workshops_api.models.user import UserModel
from workshops_api import schemas
from workshops_api import auth
from workshops_api.database import db
from workshops_api.app import app


class EventUserListResource(Resource):
    @auth.required('manage')
    def get(self, event_id, **kwargs):
        event_users = UserModel.query.filter_by(event_id=event_id)

        return {
            "users": [schemas.user_schema.dump(user).data for user in event_users]
        }

    # Security: anyone who can run this method can give themselves full admin rights!
    @auth.required('manage')
    def put(self, event_id, **kwargs):
        # This event replaces the entire event users collection, so first everything is deleted
        UserModel.query.filter_by(event_id=event_id).delete()
        db.session.commit()

        # User objects are remade here, either without ID (create new)
        # or with ID (old unchanged user)

        users_data = request.get_json()

        # We need all keys to avoid collisions
        # since the key has to be quite short for user friendlyness.
        all_keys = db.session.query(UserModel.identity)

        for user_data in users_data:
            user = schemas.user_schema.load(user_data).data

            if (user.identity == ''):
                # Generate user key and retry if not unqiue
                user.identity = auth.authenticator.generateKey()
                while (user.identity,) in all_keys:
                    user.identity = auth.authenticator.generateKey()

            db.session.add(user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            abort(
                400,
                description="Duplicate user identity key"
            )

        auth_user = kwargs['auth_user']
        app.logger.info(
            f"{auth_user.id}:{auth_user.full_name} ({request.remote_addr})"
            f"replaced user list on eventID {event_id}"
        )
        return '', 204


class UnregisteredEventUserListResource(Resource):
    @auth.required('manage')
    def get(self, event_id, **kwargs):
        unregistered_event_users = UserModel.query\
            .filter(event_id == event_id, ~UserModel.registrations.any())

        return {
            "users": [schemas.user_schema.dump(user).data for user in unregistered_event_users]
        }
