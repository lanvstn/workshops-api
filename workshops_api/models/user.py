from workshops_api.database import db
from workshops_api.models.registration import RegistrationModel


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80))
    identity = db.Column(db.String(80), unique=True)
    permission = db.Column(db.Integer, default=1)
    targetGroup = db.Column(db.String)
    event_id = db.Column(db.Integer, default=-1)
    user_class = db.Column(db.String)
    registrations = db.relationship(RegistrationModel, backref='user', lazy=True)
