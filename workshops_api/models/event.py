from workshops_api.database import db
from workshops_api.models.workshop import WorkshopModel


class EventModel(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    available = db.Column(db.Boolean)
    workshops = db.relationship(WorkshopModel, backref='event', lazy=True,
                                cascade="all,delete-orphan")
