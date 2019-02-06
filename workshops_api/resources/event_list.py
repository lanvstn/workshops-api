from flask_restful import Resource, request
from sqlalchemy.orm import raiseload

from workshops_api.models.event import EventModel
from workshops_api import auth
from workshops_api import schemas
from workshops_api.database import db
from workshops_api.app import app


class EventListResource(Resource):
    def get(self):
        event_list = EventModel.query.options(raiseload('workshops')).all()

        return {
            "events": [
                schemas.event_schema_without_workshops.dump(event).data
                for event in event_list
            ]
        }

    @auth.required('manage')
    def post(self, **kwargs):
        data = request.get_json()
        event = schemas.event_schema_without_workshops.load(data).data
        db.session.add(event)
        db.session.commit()

        response = schemas.event_schema.dump(event).data

        auth_user = kwargs['auth_user']
        app.logger.info(
            f"{auth_user.id}:{auth_user.full_name} ({request.remote_addr}) "
            f"posted event {str(event.id)}:{str(event.name)}"
        )

        return response
