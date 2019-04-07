from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from werkzeug.datastructures import MultiDict

from application import app, db
from application.map.models import Map
from application.hex.models import Hex
from application.map.forms import NewMapForm, EditMapForm
from sqlalchemy import update

import json

@app.route("/map/<map_id>", methods=["GET"])
def map_view(map_id):
	found_map = Map.query.get(map_id)

	if found_map != None and found_map.private and found_map.account_id != None and found_map.account_id != current_user.get_id():
		found_map = None
	if found_map != None:
		map_hexes = db.engine.execute("SELECT * FROM hex WHERE map_id=" + str(map_id))
		jns = {}
		for hx in map_hexes:
			if hx.x >= found_map.width + (hx.y % 2) or hx.y >= found_map.height:
				continue
			jns[str(hx.x + hx.y * (found_map.width + 1))] = str(hx.hex_type)
		return render_template("map/map.html", found_map = found_map, hexes = jns, hexes_str = json.dumps(jns), form = EditMapForm(formdata=MultiDict({'name':found_map.name, 'private': found_map.private, 'width':found_map.width, 'height':found_map.height})))
	else:
		return render_template("map/map.html", found_map = found_map, hexes = {}, hexes_str = "{}", form = EditMapForm())
		

@app.route("/map/new/", methods=["GET","POST"])
def map_new():
	if request.method == "GET":
		return render_template("map/new.html", form = NewMapForm())

	form = NewMapForm(request.form)
	if not form.validate():
		return render_template("/map/new.html", form = form)

	m = Map(form.name.data, form.private.data, form.width.data, form.height.data, current_user.get_id())

	db.session().add(m)
	db.session().commit()
	return redirect("/map/" + str(m.id))

@app.route("/map/<map_id>/edit", methods=["POST"])
def map_edit(map_id):
	# TODO: check for permissions
	form = EditMapForm(request.form)
	m = Map.query.get(map_id)
	if not form.validate() or not m:
		return render_template("/map/map.html", found_map = m, form = form)
		
	m.name = form.name.data
	m.private = form.private.data
	m.width = form.width.data
	m.height = form.height.data

	db.session().commit()
	return redirect("/map/" + str(map_id))

@app.route("/map/<map_id>/delete", methods=["POST"])
def map_delete(map_id):
	# TODO: check for permissions
	m = Map.query.get(map_id)
	if not m:
		return redirect("/map/" + str(map_id))

	db.session().delete(m)
	db.session().commit()
	return redirect("/")

@app.route("/map/<map_id>/save", methods=["POST"])
def map_save(map_id):
	jsn = request.get_json()

	m = Map.query.get(map_id)
	w = m.width
	h = m.height

	# Check that the json is valid
	try:
		for key, value in jsn.items():
			if int(key) < 0 or int(key) >= (w+1)*h:
				return redirect("/")
			elif int(value) < 1 or int(value) > 2:
				return redirect("/")
	except ValueError:
		return redirect("/")

	# Remove old data
	db.session().query(Hex).filter(Hex.map_id == str(map_id)).delete()
	# db.engine.execute("SELECT * FROM hex WHERE map_id=" + str(map_id)).delete()

	# Store the data
	for key, value in jsn.items():
		x = int(key) % (w+1)
		y = int(key) // (w+1)
		h = Hex(x, y, int(value), map_id)
		db.session().add(h)

	db.session().commit()	
	return redirect("/")
