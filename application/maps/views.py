from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from werkzeug.datastructures import MultiDict

from application import app, db
from application.maps.models import Map
from application.maps.forms import NewMapForm, EditMapForm
from sqlalchemy import update

@app.route("/maps/<map_id>", methods=["GET"])
def maps_view(map_id):
	found_map = Map.query.get(map_id)

	if found_map != None and found_map.private and found_map.account_id != None and found_map.account_id != current_user.get_id():
		found_map = None
	
	if found_map != None:
		return render_template("maps/map.html", found_map = found_map, form = EditMapForm(formdata=MultiDict({'name':found_map.name, 'private': found_map.private})))
	else:
		return render_template("maps/map.html", found_map = found_map, form = EditMapForm())
		

@app.route("/maps/new/", methods=["GET","POST"])
def maps_new():
	if request.method == "GET":
		return render_template("maps/new.html", form = NewMapForm())

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
	# TODO: check for permissions
	form = EditMapForm(request.form)
	m = Map.query.get(map_id)
	if not form.validate() or not m:
		return render_template("/maps/map.html", found_map = m, form = form)
		
	m.name = form.name.data
	m.private = form.private.data

	db.session().commit()
	return redirect("/maps/" + str(map_id))

@app.route("/maps/delete/<map_id>", methods=["POST"])
def maps_delete(map_id):
	# TODO: check for permissions
	m = Map.query.get(map_id)
	if not m:
		return redirect("/maps/" + str(map_id))

	db.session().delete(m)
	db.session().commit()
	return redirect("/")
