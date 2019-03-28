from flask import render_template, request, redirect, url_for
from application import app, db
from application.maps.models import Map
from application.maps.forms import NewMapForm, EditMapForm
from sqlalchemy import update

@app.route("/maps/<map_id>", methods=["GET"])
def maps_view(map_id):
	return render_template("maps/map.html", found_map = Map.query.get(map_id), form = EditMapForm())

@app.route("/maps/new/")
def maps_form():
	return render_template("maps/new.html", form = NewMapForm())

@app.route("/maps/", methods=["POST"])
def maps_create():
	form = NewMapForm(request.form)
	m = Map(form.name.data)
	db.session().add(m)
	db.session().commit()
	return redirect("/maps/" + str(m.id))

@app.route("/maps/edit/", methods=["POST"])
def maps_edit():
	form = EditMapForm(request.form)
	m = Map.query.get(int(form.map_id.data))
	m.name = form.name.data
	db.session().commit()
	return redirect("/maps/" + str(m.id))
