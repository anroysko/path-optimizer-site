from flask import render_template, request, redirect, url_for
from application import app, db
from application.maps.models import Map
from sqlalchemy import update

@app.route("/")
def index():
	maps = Map.query.all()
	return render_template("index.html", maps=maps)
