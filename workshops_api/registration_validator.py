from flask_restful import abort

from workshops_api.models.workshop import WorkshopModel
from workshops_api.models.registration import RegistrationModel


class RegistrationValidator:
    """ Server side validation for user registrations """

    def __init__(self, user, inputIds):
        # Get all neccesary data for the validator. DB queries only happen here.
        self.user = user
        self.inputIds = inputIds

        self.workshops = WorkshopModel.query.filter(WorkshopModel.id.in_(inputIds)).all()

        self.user_registrations = RegistrationModel.query.filter_by(user_id=self.user.id).all()

    def _event_closed(self):
        if not self.workshops[0].event.available:
            abort(
                403,
                description="Registration for this event is not allowed"
            )

    def _own_event(self):
        # Checking only first event is OK, if there are other events _same_event will fail.
        firstEventId = self.workshops[0].event_id
        if firstEventId != self.user.event_id:
            abort(
                403,
                description="You can only register for your own event"
            )

    def _reg_count(self):
        for workshop in self.workshops:
            if len(workshop.registrations) >= workshop.limit:
                abort(
                    403,
                    description="Limit reached. Refresh the page."
                )

    def _same_event(self):
        firstEventId = self.workshops[0].event_id
        for w in self.workshops:
            if w.event_id != firstEventId:
                abort(
                    403,
                    description="Not allowed to register for multiple events in one request."
                )

    def _targetGroup(self):
        for w in self.workshops:
            if w.targetGroup != self.user.targetGroup:
                abort(
                    403,
                    description="Not allowed to register for workshops outside of target group."
                )

    def _existing_registration(self):
        for r in self.user_registrations:
            if r.workshop_id in self.inputIds:
                abort(
                    409,
                    description="Already registered for this workshop."
                )

    def _one_per_moment(self):
        moments = []
        for w in self.workshops:
            if w.moment not in moments:
                moments.append(w.moment)
            else:
                abort(
                    409,
                    description="Already registered for another workshop on this moment"
                )

    def _links(self):
        for w in self.workshops:
            if hasattr(w, 'workshop_links'):
                for link in w.workshop_links:
                    if link.link_type == "inclusive":
                        if link.workshop2_id not in self.inputIds:
                            abort(
                                403,
                                description=f"Link between workshopID {link.workshop2_id} "
                                            f"and {w.id}, type: inclusive"
                            )
                    elif link.link_type == "exclusive":
                        if link.workshop2_id in self.inputIds:
                            abort(
                                403,
                                description=f"Link between workshopID {link.workshop2_id} "
                                            f"and {w.id}, type: exclusive"
                            )

    def validate(self):
        try:
            self._event_closed()
            self._own_event()
            self._same_event()
            self._reg_count()
            self._targetGroup()
            self._existing_registration()
            self._one_per_moment()
            self._links()
        except IndexError:
            # No data to validate
            abort(
                400,
                description="No data"
            )
