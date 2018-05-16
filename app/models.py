from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


'''
This class contains class definitions that extend db.Model and define tables in our database. 
'''

@login.user_loader
def load_admin(id):
    '''
    This function exists to support the needs of flask_login.
    '''
    return Admin.query.get(int(id))


class Admin(UserMixin, db.Model):
    '''
    The Admin table will store each adminitrative user account as one row, and contain 
    a mapping to all the workshops that administrator has created, in addition to some
    requisite user info.
    
    This class extends UserMixin in addition to db.Model in order to support the 
    log in and log out features of flask-login. 
    Administrators are the only users whose login status we care about. 
    Extending UserMixin inherits properties and methods that are necessary to support authentication.
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    workshops_created = db.relationship(
        'WorkshopActivity', backref='creator', lazy='dynamic')

    def set_password(self, password):
        '''
        Saves a hash of the user's plaintext password.
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''
        Hashes the password attempt and compares it to the original password's hash.
        '''
        return check_password_hash(self.password_hash, password)


class WorkshopActivity(db.Model):
    '''
    The WorkshopActivity table will contain one row for each workshop timeline created. 
    
    '''
    id = db.Column(db.Integer, primary_key=True)
    unique_str = db.Column(db.String(20), unique=True, index=True)
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    question = db.Column(db.String(140))
    unit_is_year = db.Column(db.Boolean(), default=False)
    admin_owner = db.Column(db.Integer, db.ForeignKey("admin.id"))
    postits = db.relationship('PostIt', backref='session', lazy='dynamic')
    active = db.Column(db.Boolean(), default=True)
    enable_monitoring = db.Column(db.Boolean(), default=False)


class PostIt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    year_timestamp = db.Column(db.Integer())
    mdy_timestamp = db.Column(db.Date, index=True)
    on_sex = db.Column(db.Boolean(), default=True)
    session_id = db.Column(db.Integer, db.ForeignKey('workshop_activity.id'))
    approved = db.Column(db.Boolean(), default=True)
