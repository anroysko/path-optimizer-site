from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField

class NewMapForm(FlaskForm):
	name = StringField("Map name")
	private = BooleanField("Private")
	class Meta:
		csrf = False

class EditMapForm(FlaskForm):
	name = StringField("New name")
	map_id = IntegerField("Map ID (TODO: do not ask this)")
	class Meta:
		csrf = False
