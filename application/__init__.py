#Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Import the database
import os
if os.environ.get("HEROKU"):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
	app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

#Site-specific functionality
from application import views
from application.map import models
from application.map import views
from application.auth import models
from application.auth import views
from application.hex import models

#Logging in
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality"

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

#Create tables if needed
try:
	db.create_all()
except:
	pass
