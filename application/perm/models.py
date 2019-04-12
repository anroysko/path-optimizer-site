from application import db

class Perm(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
	map_id = db.Column(db.Integer, db.ForeignKey('map.id'))
	view_perm = db.Column(db.Boolean, nullable=False, default=False)
	edit_perm = db.Column(db.Boolean, nullable=False, default=False)

	def __init__(self, account_id, map_id, view_perm, edit_perm):
		self.account_id = account_id
		self.map_id = map_id
		self.view_perm = view_perm
		self.edit_perm = edit_perm
