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
	return db.engine.execute(q, i = account_id).fetchall()

def get_shared_maps(account_id):
	q = text("SELECT Map.*"
		" FROM MAP"
		" LEFT JOIN PERM"
		" ON Perm.map_id = Map.id"
		" WHERE (Perm.view_perm AND NOT Perm.owner_perm AND Perm.account_id = :i)"
		" GROUP BY Map.id"
		" HAVING COUNT(Perm.id) > 0")
	return db.engine.execute(q, i = account_id).fetchall()

# Get all accounts with the given perms on the map
def get_map_accounts(map_id, view_perm, edit_perm):
	q = text("SELECT Account.*"
		" FROM ACCOUNT"
		" LEFT JOIN PERM"
		" ON Perm.account_id = Account.id"
		" WHERE (Perm.view_perm = :i AND Perm.edit_perm = :j AND Perm.map_id = :mi)"
		" GROUP BY Account.id"
		" HAVING COUNT(Perm.id) > 0")
	return db.engine.execute(q, i = view_perm, j = edit_perm, mi = map_id).fetchall()

def get_all_map_perms(map_id):
	q = text("SELECT Perm.* FROM PERM WHERE Perm.map_id = :mi")
	return db.engine.execute(q, mi = map_id).fetchall()

def change_perms(m, usr, view_perm, edit_perm):
	perm = Perm.query.filter(Perm.map_id == m.id, Perm.account_id == usr.id).first()
	if perm == None:
		# Create a new perm
		print("!!!!!!!!!!! CREATE NEW PERM")
		new_perm = Perm(usr.id, m.id, view_perm, edit_perm, False)
		db.session().add(new_perm)
	else:
		print("!!!!!!!!!!! CHANGE PERM " + str(perm.id) + " PERMS!")
		perm.view_perm = view_perm
		perm.edit_perm = edit_perm
	db.session().commit()
