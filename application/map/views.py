from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from werkzeug.datastructures import MultiDict

from flask import abort
from application import app, db, login_manager
from application.map.models import Map
from application.hex.models import Hex
from application.map.forms import NewMapForm, EditMapForm, SearchMapForm
from application.perm.queries import get_account_map_perms, get_map_accounts
from application.hex.queries import get_map_hexes, build_hex_map
from application.map.queries import make_new_map, edit_map, delete_map, save_map
from sqlalchemy import update
import json

@app.route("/map/<map_id>", methods=["GET"])
def map_view(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)

	# Get user perms on the map
	view_perm, edit_perm, owner_perm = get_account_map_perms(current_user.get_id(), map_id)
	if not view_perm:
		return render_template("map/map.html", view_perm=False)

	# Load hexes in the map
	jsn = build_hex_map(m)

	# Load accounts with perms on the map
	view_perm_users = get_map_accounts(map_id, True, False)
	edit_perm_users = get_map_accounts(map_id, True, True)

	# Serve the map
	return render_template("map/map.html", found_map = m, hexes = jsn, hexes_str = json.dumps(jsn), view_perm=view_perm, edit_perm=edit_perm, owner_perm=owner_perm, view_perm_users=view_perm_users, edit_perm_users=edit_perm_users, form = EditMapForm())

@app.route("/map/new/", methods=["POST"])
def map_new():
	# check that the form is valid
	form = NewMapForm(request.form)
	if not form.validate():
		return redirect("/")

	# make the new map
	m = make_new_map(form, current_user.get_id())
	return redirect("/map/" + str(m.id))

@app.route("/map/<map_id>/edit", methods=["POST"])
def map_edit(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)

	view_perm, edit_perm, owner_perm = get_account_map_perms(current_user.get_id(), map_id)
	if not edit_perm:
		return login_manager.unauthorized()

	# Check that the form is valid
	form = EditMapForm(request.form)
	if not form.validate():
		return redirect("/map/" + str(m.id))

	# Edit the map
	m = edit_map(m, form)
	return redirect("/map/" + str(m.id))

@app.route("/map/search", methods=["POST"])
def map_search():
	form = SearchMapForm(request.form)
	if not form.validate():
		return redirect("/")
	else:
		return redirect("/map/" + str(form.map_id.data))

@app.route("/map/<map_id>/delete", methods=["POST"])
def map_delete(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)
	view_perm, edit_perm, owner_perm = get_account_map_perms(current_user.get_id(), map_id)
	if not owner_perm:
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
	view_perm, edit_perm, owner_perm = get_account_map_perms(current_user.get_id(), map_id)
	if not edit_perm:
		return login_manager.unauthorized()

	fail = not save_map(m, request.get_json())
	if fail:
		abort(400) # Failure due to bad request
	else:
		return redirect("/map/" + str(m.id))

@app.route("/map/<map_id>/edit_perms/default", methods=["POST"])
def map_edit_perms_default(map_id):
	# Check that the map is valid and user has permission to modify it
	m = Map.query.get(map_id)
	if m == None:
		abort(404)

	view_perm, edit_perm, owner_perm = get_account_map_perms(current_user.get_id(), map_id)
	if not owner_perm:
		return login_manager.unauthorized()

	# Process more stuff here
	#fail = not save_map(m, request.get_json())
	#if fail:
	#	abort(400) # Failure due to bad request
	#else:
	return redirect("/map/" + str(m.id))

