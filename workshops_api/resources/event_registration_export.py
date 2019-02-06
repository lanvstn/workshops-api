from flask_restful import Resource
from flask import make_response, request
from openpyxl import Workbook
from tempfile import NamedTemporaryFile

from workshops_api.models.workshop import WorkshopModel
from workshops_api import auth
from workshops_api.app import app


class EventRegistrationExportResource(Resource):
    @auth.required('manage')
    def get(self, event_id, **kwargs):
        workshops = WorkshopModel.query.filter_by(event_id=event_id)

        wb = Workbook(write_only=True)

        for workshop in workshops:
            # New sheet
            workshop_sheet = wb.create_sheet(workshop.title)
            workshop_sheet.append([workshop.title])
            workshop_sheet.append([''])
            workshop_sheet.append(['Naam', 'Klas'])

            for registration in workshop.registrations:
                # New row
                workshop_sheet.append([registration.user.full_name, registration.user.user_class])

        # Save XLSX file read it (no way to do this without writing a file)
        with NamedTemporaryFile() as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            data = tmp.read()

        response = make_response(data)
        response.headers['Content-Type'] = 'application/' \
                                           'vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        auth_user = kwargs['auth_user']
        app.logger.info(
            f"{auth_user.id}:{auth_user.full_name} ({request.remote_addr}) "
            f"exported event registration list for eventID {event_id}"
        )

        return response
