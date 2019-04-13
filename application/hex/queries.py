from application import db
from application.perm.models import Perm
from sqlalchemy.sql import text

def get_map_hexes(map_id):
	q = text("SELECT * FROM hex WHERE map_id=:i")
	return db.engine.execute(q, i=map_id).fetchall()

def delete_map_hexes(map_id):
	q = text("DELETE FROM hex WHERE map_id=:i")
	db.engine.execute(q, i=map_id)
	db.session.commit()

def build_hex_map(m):
	q = text("SELECT * FROM hex WHERE map_id=:i")
	map_hexes = db.engine.execute(q,i=m.id)

	jns = {}
	for hx in map_hexes:
		if hx.x >= m.width + (hx.y % 2) or hx.y >= m.height:
			continue
		jns[str(hx.x + hx.y * (m.width + 1))] = str(hx.hex_type)
	return jns
