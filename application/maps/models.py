from application import db

class Map(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(144), nullable=False)
	private = db.Column(db.Boolean, nullable=False, default=False)
	owner = db.Column(db.Integer)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	def __init__(self, name):
		self.name = name
		
		self.done = False
