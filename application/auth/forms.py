from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
	username = StringField("Username")
	password = PasswordField("Password")

	class Meta:
		csrf = False

class RegisterForm(FlaskForm):
	username = StringField("Username", [validators.Length(min=1)])
	password = PasswordField("Password")

	class Meta:
		csrf = False
