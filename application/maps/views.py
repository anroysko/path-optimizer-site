from flask import render_template, request, redirect, url_for
from application import app, db
from application.maps.models import Map
from sqlalchemy import update

@app.route("/maps/<map_id>", methods=["GET"])
def maps_view(map_id):
	return render_template("maps/map.html", found_map = Map.query.get(map_id))

@app.route("/maps/new/")
def maps_form():
	return render_template("maps/new.html")

@app.route("/maps/", methods=["POST"])
def maps_create():
	m = Map(request.form.get("name"))
	db.session().add(m)
	db.session().commit()
	return redirect("/maps/" + str(m.id))

@app.route("/maps/edit/", methods=["POST"])
def maps_edit():
	m = Map.query.get(int(request.form.get("map_id")))
	m.name = request.form.get("name")
	db.session().commit()
	return redirect("/maps/" + str(m.id))