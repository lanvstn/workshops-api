from workshops_api.database import db
from workshops_api.models.registration import RegistrationModel


class WorkshopModel(db.Model):
    __tablename__ = "workshop"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), default="Workshop", nullable=False)
    description = db.Column(db.Text, default="")
    moment = db.Column(db.String(80), default="default", nullable=False)
    limit = db.Column(db.Integer, default=1000, nullable=False)
    targetGroup = db.Column(db.String(80), default="", nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registrations = db.relationship(RegistrationModel, lazy=True, cascade='all,delete-orphan')
