from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from werkzeug.datastructures import MultiDict

from flask import abort
from application import app, db, login_manager
from application.map.models import Map
from application.hex.models import Hex
from application.map.forms import NewMapForm, EditMapForm
from application.perm.queries import get_account_map_perms
from application.hex.queries import get_map_hexes
from sqlalchemy import update

import application.map.queries
import json

@app.route("/map/<map_id>", methods=["GET"])
def map_view(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)

	view_perm, edit_perm, owner_perm = get_account_map_perms(current_user.get_id(), map_id)
	if not view_perm:
		return render_template("map/map.html", view_perm=False)
		return login_manager.unauthorized()

	# Load hexes in the map
	jsn = build_hex_map(m)

	# Serve the map
	return render_template("map/map.html", found_map = m, hexes = jsn, hexes_str = json.dumps(jsn), view_perm=view_perm, edit_perm=edit_perm, owner_perm=owner_perm, form = EditMapForm())

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
	m = make_new_map(form)
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
	m = edit_map(m, form)
	return redirect("/map/" + str(m.id))

@app.route("/map/<map_id>/delete", methods=["POST"])
def map_delete(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)
	if (m.private) and (m.account_id != None) and (m.account_id != current_user.get_id()):
		return login_manager.unauthorized()

	# Delete the map
	delete_map(m)
	return redirect("/")

@app.route("/map/<map_id>/save", methods=["POST"])
def map_save(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)
	if (m.private) and (m.account_id != None) and (m.account_id != current_user.get_id()):
		return login_manager.unauthorized()

	fail = not save_map(m, request.get_json)
	if fail:
		abort(400) # Failure due to bad request
	else:
		return redirect("/map/" + str(m.id))
