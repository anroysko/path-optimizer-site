#Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Import the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maps.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

#Site-specific functionality
from application import views
from application.maps import models
from application.maps import views
from application.auth import models
from application.auth import views

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
db.create_all()
