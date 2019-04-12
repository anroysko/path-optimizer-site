from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from werkzeug.datastructures import MultiDict

from flask import abort
from application import app, db, login_manager
from application.map.models import Map
from application.hex.models import Hex
from application.map.forms import NewMapForm, EditMapForm
from sqlalchemy import update

import json

@app.route("/map/<map_id>", methods=["GET"])
def map_view(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)
	if (m.private) and (m.account_id != None) and (m.account_id != current_user.get_id()):
		return login_manager.unauthorized()

	# Load hexes in the map
	map_hexes = db.engine.execute("SELECT * FROM hex WHERE map_id=" + str(map_id))
	jns = {}
	for hx in map_hexes:
		if hx.x >= m.width + (hx.y % 2) or hx.y >= m.height:
			continue
		jns[str(hx.x + hx.y * (m.width + 1))] = str(hx.hex_type)

	# Serve the map
	return render_template("map/map.html", found_map = m, hexes = jns, hexes_str = json.dumps(jns), form = EditMapForm(formdata=MultiDict({'name': m.name, 'private': m.private, 'width': m.width, 'height': m.height})))
		

@app.route("/map/new/", methods=["GET","POST"])
def map_new():
	# serve the new map page if requested
	if request.method == "GET":
		return render_template("map/new.html", form = NewMapForm())

	# check that the form is valid
	form = NewMapForm(request.form)
	if not form.validate():
		return render_template("/map/new.html", form = form)

	# make the new map
	m = Map(form.name.data, form.private.data, form.width.data, form.height.data, current_user.get_id())

	db.session().add(m)
	db.session().commit()
	return redirect("/map/" + str(m.id))

@app.route("/map/<map_id>/edit", methods=["POST"])
def map_edit(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)
	if (m.private) and (m.account_id != None) and (m.account_id != current_user.get_id()):
		return login_manager.unauthorized()

	# Check that the form is valid
	form = EditMapForm(request.form)
	if not form.validate():
		return render_template("/map/map.html", found_map = m, form = form)

	# Edit the map
	m.name = form.name.data
	m.private = form.private.data
	m.width = form.width.data
	m.height = form.height.data

	db.session().commit()
	return redirect("/map/" + str(map_id))

@app.route("/map/<map_id>/delete", methods=["POST"])
def map_delete(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)
	if (m.private) and (m.account_id != None) and (m.account_id != current_user.get_id()):
		return login_manager.unauthorized()

	# Delete the map
	db.session().delete(m)
	db.session().commit()
	return redirect("/")

@app.route("/map/<map_id>/save", methods=["POST"])
def map_save(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)
	if (m.private) and (m.account_id != None) and (m.account_id != current_user.get_id()):
		return login_manager.unauthorized()
	w = m.width
	h = m.height

	# Check that the json is valid
	jsn = request.get_json()
	try:
		for key, value in jsn.items():
			if int(key) < 0 or int(key) >= (w+1)*h:
				return redirect("/")
			elif int(value) < 1 or int(value) > 2:
				return redirect("/")
	except ValueError:
		abort(400) # Bad request

	# Remove old data
	db.session().query(Hex).filter(Hex.map_id == str(map_id)).delete()

	# Store new data
	for key, value in jsn.items():
		x = int(key) % (w+1)
		y = int(key) // (w+1)
		h = Hex(x, y, int(value), map_id)
		db.session().add(h)

	db.session().commit()
	return redirect("/")
