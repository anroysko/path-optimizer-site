from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.maps.models import Map
from sqlalchemy import update

@app.route("/")
def index():
	public_maps = db.engine.execute("SELECT * FROM map WHERE private=False")
	if current_user.get_id():
		user_maps = db.engine.execute("SELECT * FROM map WHERE account_id=" + str(current_user.get_id()))
		return render_template("index.html", public_maps=public_maps, user_maps=user_maps)
	else:
		return render_template("index.html", public_maps=public_maps)
