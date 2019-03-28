from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.maps.models import Map
from application.maps.forms import NewMapForm, EditMapForm
from sqlalchemy import update

@app.route("/maps/<map_id>", methods=["GET"])
def maps_view(map_id):
	found_map = Map.query.get(map_id)

	# Hacked way to not show a private map you are not the owner of
	# Note that you can still currently edit private maps you don't own :P
	if found_map != None and found_map.private and found_map.account_id != None and found_map.account_id != current_user.get_id():
		found_map = None

	return render_template("maps/map.html", found_map = found_map, form = EditMapForm())

@app.route("/maps/new/")
def maps_form():
	return render_template("maps/new.html", form = NewMapForm())

@app.route("/maps/", methods=["POST"])
def maps_create():
	form = NewMapForm(request.form)
	if not form.validate():
		return render_template("/maps/new.html", form = form)

	m = Map(form.name.data)
	m.private = form.private.data
	m.account_id = current_user.get_id()

	db.session().add(m)
	db.session().commit()
	return redirect("/maps/" + str(m.id))

@app.route("/maps/edit/<map_id>", methods=["POST"])
def maps_edit(map_id):
	form = EditMapForm(request.form)
	if not form.validate():
		found_map = Map.query.get(map_id)
		return render_template("/maps/map.html", found_map = found_map, form = form)

	m = Map.query.get(map_id) #TTETT m isn't null
	m.name = form.name.data
	db.session().commit()
	return redirect("/maps/" + str(map_id))
