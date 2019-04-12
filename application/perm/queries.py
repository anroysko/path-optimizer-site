from application import db
from application.perm.models import Perm
from sqlalchemy.sql import text, query

def get_account_map_perms(account_id, map_id):
	q = text("SELECT Perm.* FROM PERM WHERE Perm.account_id = :ai AND Perm.map_id = :mi")
	p = db.engine.execute(q, ai=account_id, mi=map_id).fetchone()
	if p == None:
		assert account_id, "All maps should have a permissions entry for None user. map_id: " + str(map_id) + "."
		return get_account_map_perms(None, map_id)
	return p.view_perm, p.edit_perm, p.owner_perm

def get_owned_maps(account_id):
	q = text("SELECT Map.*"
			" FROM MAP"
			" LEFT JOIN PERM"
			" ON Map.id = Perm.map_id"
			" WHERE (Perm.owner_perm AND Perm.account_id = :i)"
			" GROUP BY Map.id")
	return db.engine.execute(q, i = account_id)

def get_shared_maps(account_id):
	q = text("SELECT Map.*"
		" FROM MAP"
		" LEFT JOIN PERM"
		" ON Map.id = Perm.map_id"
		" WHERE (Perm.view_perm AND NOT Perm.owner_perm AND Perm.account_id = :i)"
		" GROUP BY Map.id")
	return db.engine.execute(q, i = account_id)

