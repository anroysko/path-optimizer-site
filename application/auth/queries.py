from application import db
from sqlalchemy.sql import text

from application.auth.models import User, encrypt_password, check_password

def get_user(username, password=None):
	if password is None:
		return User.query.filter_by(username=username).first()
	else:
		user = User.query.filter_by(username=username).first()
		if user is not None:
			if check_password(user._password, password):
				return user
		return None
