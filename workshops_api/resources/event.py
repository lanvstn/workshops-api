from flask_restful import Resource, request

from workshops_api.models.event import EventModel
from workshops_api.models.registration import RegistrationModel
from workshops_api import auth
from workshops_api import schemas
from workshops_api.database import db
from workshops_api.app import app


class EventResource(Resource):
    def get(self, event_id):
        event = EventModel.query.get(event_id)

        response = schemas.event_schema.dump(event).data
        self._addRegistrationCount(response)

        return response

    @auth.required('manage')
    def put(self, event_id, **kwargs):
        data = request.get_json()
        event = schemas.event_schema.load(data).data

        db.session.merge(event)
        db.session.commit()

        response = schemas.event_schema.dump(event).data
        self._addRegistrationCount(response)

        return response

    @auth.required('manage')
    def delete(self, event_id, **kwargs):
        EventModel.query.get(event_id).delete()

        auth_user = kwargs['auth_user']
        app.logger.info(
            f"{auth_user.id}:{auth_user.full_name} ({request.remote_addr}) "
            f"deleted eventID {str(event_id)}"
        )

        return {}, 204

    def _addRegistrationCount(self, response):
        """ Add registration count to response """
        for workshop in response['workshops']:
            count = RegistrationModel.query.filter_by(workshop_id=workshop['id']).count()
            workshop['_registrationCount'] = count
