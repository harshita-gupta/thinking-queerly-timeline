from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

'''
Flask app configuration and add-on setup.
'''


app = Flask(__name__)
app.config.from_object(Config)

# DB and DB migration libraries.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login managers
login = LoginManager(app)
login.login_view = 'login'

# Bootstrap add-on for styling
bootstrap = Bootstrap(app)

from app import routes, models, errors
