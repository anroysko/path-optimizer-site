from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, validators

class NewMapForm(FlaskForm):
	name = StringField("Map name", [validators.Length(min=1)])
	width = IntegerField("Map width", [validators.DataRequired(), validators.NumberRange(1, 100)])
	height = IntegerField("Map height", [validators.DataRequired(), validators.NumberRange(1, 100)])

	class Meta:
		csrf = False

class EditMapForm(FlaskForm):
	name = StringField("New name", [validators.Length(min=1)])
	width = IntegerField("Map width", [validators.DataRequired(), validators.NumberRange(1, 100)])
	height = IntegerField("Map height", [validators.DataRequired(), validators.NumberRange(1, 100)])

	class Meta:
		csrf = False

class SearchMapForm(FlaskForm):
	map_id = IntegerField("Map ID", [validators.DataRequired(), validators.NumberRange(min=1)])

	class Meta:
		csrf = False
