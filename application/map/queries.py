from application import db
from sqlalchemy.sql import text

from application.map.models import Map
from application.perm.models import Perm
from application.hex.models import Hex
from application.hex.queries import delete_map_hexes
from application.map.forms import NewMapForm, EditMapForm

def make_new_map(form, account_id):
	m = Map(form.name.data, form.width.data, form.height.data)
	db.session().add(m)
	db.session().commit()

	# Add perms
	if account_id:
		p1 = Perm(account_id, m.id, True, True, True)
		p2 = Perm(None, m.id, True, False, False) # TODO: set according to "private?" here
		db.session().add(p1)
		db.session().add(p2)
	else:
		p1 = Perm(None, m.id, True, True, True)
		db.session().add(p1)
	db.session().commit()

	return m

def edit_map(m, form):
	m.name = form.name.data
	m.width = form.width.data
	m.height = form.height.data

	db.session().commit()
	return m

def delete_map(m):
	db.session().delete(m)
	db.session().commit()

def save_map(m, jsn):
	# Check data
	w = m.width
	h = m.height

	try:
		for key, value in jsn.items():
			if int(key) < 0 or int(key) >= (w+1)*h:
				return False
			elif int(value) < 1 or int(value) > 2:
				return False
	except ValueError:
		return False; # Value not int

	# Overwrite data
	delete_map_hexes(m.id)
	for key, value in jsn.items():
		x = int(key) % (w+1)
		y = int(key) // (w+1)
		h = Hex(x, y, int(value), m.id)
		db.session().add(h)

	db.session().commit()
	return True