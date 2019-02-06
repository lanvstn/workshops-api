from flask_restful import Resource
from flask import request
from datetime import datetime

from workshops_api.models.registration import RegistrationModel
from workshops_api import auth
from workshops_api.database import db
from workshops_api.registration_validator import RegistrationValidator
from workshops_api import schemas
from workshops_api.app import app


class RegistrationUserResource(Resource):
    @auth.required('user')
    @auth.restrict_to_self()
    def get(self, user_id, **kwargs):
        registrations = RegistrationModel.query.filter_by(user_id=user_id).all()

        return {
            "registrations": [
                schemas.registration_schema.dump(registration).data
                for registration in registrations
            ]
        }

    @auth.required('user')
    @auth.restrict_to_self()
    def put(self, user_id, **kwargs):
        RegistrationModel.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        workshop_ids = request.get_json()['workshop_ids']

        rv = RegistrationValidator(
            auth.verify_request(request),
            workshop_ids
        )
        rv.validate()

        for workshop_id in workshop_ids:
            db.session.add(RegistrationModel(
                entry_time=datetime.now(),
                workshop_id=workshop_id,
                user_id=user_id
            ))

        db.session.commit()

        auth_user = kwargs['auth_user']
        app.logger.info(
            f"{auth_user.id}:{auth_user.full_name} ({request.remote_addr}) "
            f"registered for {str(workshop_ids)}"
        )

        return self.get(user_id=user_id)

    @auth.required('user')
    @auth.restrict_to_self()
    def delete(self, user_id, workshop_id, **kwargs):
        deleteRegistration = RegistrationModel.query.filter_by(
            user_id=user_id,
            workshop_id=workshop_id
        ).first()

        db.session.delete(deleteRegistration)
        db.session.commit()

        auth_user = kwargs['auth_user']
        app.logger.info(
            f"{auth_user.id}:{auth_user.full_name} ({request.remote_addr}) "
            f"deleted registration userID:{str(user_id)} workshopID:{str(workshop_id)}"
        )

        return '', 204
