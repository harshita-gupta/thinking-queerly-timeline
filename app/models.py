from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_admin(id):
    return Admin.query.get(int(id))


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    workshops_created = db.relationship(
        'WorkshopActivity', backref='creator', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class WorkshopActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_str = db.Column(db.String(20), unique=True, index=True)
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    question = db.Column(db.String(140))
    unit_is_year = db.Column(db.Boolean(), default=False)
    admin_owner = db.Column(db.Integer, db.ForeignKey("admin.id"))
    postits = db.relationship('PostIt', backref='session', lazy='dynamic')


class PostIt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    year_timestamp = db.Column(db.Integer())
    mdy_timestamp = db.Column(db.Date, index=True)
    on_sex = db.Column(db.Boolean(), default=True)
    session_id = db.Column(db.Integer, db.ForeignKey('workshop_activity.id'))
