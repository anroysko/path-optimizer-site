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
def get_map_accounts(map_id, view_perm, edit_perm, owner_perm):
	q = text("SELECT Account.*"
		" FROM ACCOUNT"
		" LEFT JOIN PERM"
		" ON Perm.account_id = Account.id"
		" WHERE (Perm.view_perm = :i AND Perm.edit_perm = :j AND Perm.owner_perm = :k AND Perm.map_id = :mi)"
		" GROUP BY Account.id"
		" HAVING COUNT(Perm.id) > 0")
	return db.engine.execute(q, i = view_perm, j = edit_perm, k = owner_perm, mi = map_id).fetchall()

def change_perms(m, usr, view_perm, edit_perm):
	usr_id = None
	if usr != None:
		usr_id = usr.id

	perm = Perm.query.filter(Perm.map_id == m.id, Perm.account_id == usr_id).first()
	if perm == None:
		# Create a new perm
		new_perm = Perm(usr.id, m.id, view_perm, edit_perm, False)
		db.session().add(new_perm)
	else:
		if perm.owner_perm:
			return False; # Cannot change permissions of the owner
		perm.view_perm = view_perm
		perm.edit_perm = edit_perm

	db.session().commit()
	return True;
