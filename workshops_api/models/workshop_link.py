from workshops_api.database import db


class WorkshopLinkModel(db.Model):
    __tablename__ = "workshop_link"

    workshop1_id = db.Column(db.Integer, db.ForeignKey('workshop.id'), primary_key=True)
    workshop2_id = db.Column(db.Integer, db.ForeignKey('workshop.id'), primary_key=True)
    link_type = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
