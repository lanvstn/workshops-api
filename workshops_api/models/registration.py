from workshops_api.database import db


class RegistrationModel(db.Model):
    __tablename__ = "registration"

    id = db.Column(db.Integer, primary_key=True)
    entry_time = db.Column(db.DateTime)
    workshop_id = db.Column(db.ForeignKey('workshop.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
