from application import db

class Hex(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	
	x = db.Column(db.Integer, nullable=False)
	y = db.Column(db.Integer, nullable=False)
	hex_type = db.Column(db.Integer, nullable=False)
	map_id = db.Column(db.Integer, db.ForeignKey('map.id'), nullable=False)

	def __init__(self, x, y, hex_type, map_id):
		self.x = x
		self.y = y
		self.hex_type = hex_type
		self.map_id = map_id
