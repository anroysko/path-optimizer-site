from application import db

class Map(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	
	name = db.Column(db.String(144), nullable=False)
	width = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)
	hexes = db.relationship("Hex", backref='map', lazy=True, cascade="all, delete-orphan")

	# Private if nobody has view permissions
	# Immutable if nobody has edit permissions
	# Owner is the user with owner permissions
	perms = db.relationship("Perm", backref='map', lazy=True, cascade="all, delete-orphan")

	def __init__(self, name, width, height):
		self.name = name
		self.width = width
		self.height = height
