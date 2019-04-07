from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, validators

class NewMapForm(FlaskForm):
	name = StringField("Map name", [validators.Length(min=1)])
	private = BooleanField("Private")
	width = IntegerField("Map width", [validators.DataRequired(), validators.NumberRange(1, 10)])
	height = IntegerField("Map height", [validators.DataRequired(), validators.NumberRange(1, 10)])
	class Meta:
		csrf = False

class EditMapForm(FlaskForm):
	name = StringField("New name", [validators.Length(min=1)])
	private = BooleanField("Private")
	width = IntegerField("Map width", [validators.DataRequired(), validators.NumberRange(1, 10)])
	height = IntegerField("Map height", [validators.DataRequired(), validators.NumberRange(1, 10)])
	class Meta:
		csrf = False
