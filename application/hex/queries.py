from application import db
from application.perm.models import Perm
from sqlalchemy.sql import text, query

def get_map_hexes(map_id):
	q = text("SELECT * FROM hex WHERE map_id=:i")
	return db.engine.execute(q, i=map_id).fetchall()
