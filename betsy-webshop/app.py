from flask import Flask
from flask_login import LoginManager
from playhouse.flask_utils import FlaskDB
import os


# config for Peewee DB
DATABASE = "sqlite:///betsy.db"
SECRET_KEY = os.urandom(16).hex()

# setup FLASK
app = Flask(__name__)
app.config.from_object(__name__)


# wrapper for peewee database
db_wrapper = FlaskDB(app)
db = db_wrapper.database  # db is nu een peewee database

# flask-login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You need to be logged in to view this page."
login_manager.login_message_category = "warning"


import routes