from application import db

class Perm(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
	map_id = db.Column(db.Integer, db.ForeignKey('map.id'), nullable=False)

	# view_perm: Can view the map given the link. If the account is not None, sees the map on their index.
	# edit_perm: Can edit the map.
	# owner_perm: Can edit permissions of the map, and possibly delete it. Sees map as their own map on their index.
	view_perm = db.Column(db.Boolean, nullable=False, default=False)
	edit_perm = db.Column(db.Boolean, nullable=False, default=False)
	owner_perm = db.Column(db.Boolean, nullable=False, default=False)

	def __init__(self, account_id, map_id, view_perm, edit_perm, owner_perm):
		self.account_id = account_id
		self.map_id = map_id
		self.view_perm = view_perm
		self.edit_perm = edit_perm
		self.owner_perm = owner_perm

		assert (not edit_perm) or (view_perm), "edit_perm implies view_perm"
		assert (not owner_perm) or (edit_perm), "owner_perm implies edit_perm"
