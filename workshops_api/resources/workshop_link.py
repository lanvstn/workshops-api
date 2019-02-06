from flask_restful import Resource, request

from workshops_api.models.workshop_link import WorkshopLinkModel
from workshops_api import schemas
from workshops_api.database import db
from workshops_api import auth
from workshops_api.app import app


class WorkshopLinkResource(Resource):
    @auth.required('user')
    def get(self, event_id, **kwargs):
        workshop_links = WorkshopLinkModel.query.filter_by(event_id=event_id)

        return {
            'workshop_links': [
                schemas.workshop_link_schema.dump(workshop_link) for workshop_link in workshop_links
            ]
        }

    @auth.required('manage')
    def put(self, event_id, **kwargs):
        WorkshopLinkModel.query.filter_by(event_id=event_id).delete()
        db.session.commit()

        data = request.get_json()
        workshop_links = [
            schemas.workshop_link_schema.load(workshop_link_data).data
            for workshop_link_data in data
        ]

        for workshop_link in workshop_links:
            db.session.add(workshop_link)

        db.session.commit()

        auth_user = kwargs['auth_user']
        app.logger.info(
            f"{auth_user.id}:{auth_user.full_name} ({request.remote_addr}) "
            f"changed workshop links for eventID {str(event_id)}"
        )

        return '', 204
