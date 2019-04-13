from application import db
from application.perm.models import Perm
from sqlalchemy.sql import text

def get_account_map_perms(account_id, map_id):
	if account_id == None:
		q = text("SELECT Perm.* FROM PERM WHERE Perm.account_id IS NULL AND Perm.map_id = :mi")
		p = db.engine.execute(q, mi=map_id).fetchone()
		assert p != None, "All maps must have default perms"
		return p.view_perm, p.edit_perm, p.owner_perm
	else:
		q = text("SELECT Perm.* FROM PERM WHERE Perm.account_id = :ai AND Perm.map_id = :mi")
		p = db.engine.execute(q, ai=account_id, mi=map_id).fetchone()
		if p == None:
			return get_account_map_perms(None, map_id)
		return p.view_perm, p.edit_perm, p.owner_perm

def get_owned_maps(account_id):
	q = text("SELECT Map.*"
		" FROM MAP"
		" LEFT JOIN PERM"
		" ON Perm.map_id = Map.id"
		" WHERE (Perm.owner_perm AND Perm.account_id = :i)"
		" GROUP BY Map.id"
		" HAVING COUNT(Perm.id) > 0")
	return db.engine.execute(q, i = account_id)

def get_shared_maps(account_id):
	q = text("SELECT Map.*"
		" FROM MAP"
		" LEFT JOIN PERM"
		" ON Perm.map_id = Map.id"
		" WHERE (Perm.view_perm AND NOT Perm.owner_perm AND Perm.account_id = :i)"
		" GROUP BY Map.id"
		" HAVING COUNT(Perm.id) > 0")
	return db.engine.execute(q, i = account_id)

