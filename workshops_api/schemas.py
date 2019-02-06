from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from workshops_api.models.event import EventModel
from workshops_api.models.workshop_link import WorkshopLinkModel
from workshops_api.models.workshop import WorkshopModel
from workshops_api.models.registration import RegistrationModel
from workshops_api.models.user import UserModel
from workshops_api.database import db


class WorkshopSchema(ModelSchema):
    # Registrations are part of the Workhop model but should not be serialized since
    # the user should not be able to view other's registrations.
    registrations = fields.Constant(None, dump_only=True)

    class Meta:
        model = WorkshopModel
        sqla_session = db.session


class EventSchema(ModelSchema):
    workshops = fields.Nested(WorkshopSchema, many=True)

    class Meta:
        model = EventModel
        sqla_session = db.session


class EventSchemaWithoutWorkshops(ModelSchema):
    workshops = fields.Constant(None, dump_only=True)

    class Meta:
        model = EventModel
        sqla_session = db.session


class RegistrationSchema(ModelSchema):
    # Foreign keys are not automatically serialized
    user_id = fields.Int()
    workshop_id = fields.Int()

    class Meta:
        model = RegistrationModel
        sqla_session = db.session


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel
        sqla_session = db.session


class WorkshopLinkSchema(ModelSchema):
    # Override fields because for some reason marshmallow does not dump them if I don't
    workshop1_id = fields.Int()
    workshop2_id = fields.Int()
    link_type = fields.Str()
    event_id = fields.Int()

    class Meta:
        model = WorkshopLinkModel
        sqla_session = db.session


event_schema = EventSchema()
event_schema_without_workshops = EventSchemaWithoutWorkshops()
workshop_schema = WorkshopSchema()
registration_schema = RegistrationSchema()
user_schema = UserSchema()
workshop_link_schema = WorkshopLinkSchema()
