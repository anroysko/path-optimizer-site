from application import db

class Map(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	
	name = db.Column(db.String(144), nullable=False)
	private = db.Column(db.Boolean, nullable=False, default=False)
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

	def __init__(self, name):
		self.name = name
		self.done = False
