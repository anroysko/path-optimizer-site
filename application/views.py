from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.map.models import Map
from sqlalchemy.sql import text

from application.perm.queries import get_owned_maps, get_shared_maps

@app.route("/")
def index():
	account_id = current_user.get_id()
	if not account_id:
		return render_template("index.html")
	else:
		owned_maps = get_owned_maps(account_id)
		shared_maps = get_shared_maps(account_id)
		return render_template("index.html", owned_maps=owned_maps, shared_maps=shared_maps)
