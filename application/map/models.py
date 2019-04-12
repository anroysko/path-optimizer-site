from application import db

class Map(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	
	name = db.Column(db.String(144), nullable=False)
	private = db.Column(db.Boolean, nullable=False, default=False)
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

	width = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)
	hexes = db.relationship("Hex", backref='map', lazy=True, cascade="all, delete-orphan")
	perms = db.relationship("Perm", backref='map', lazy=True, cascade="all, delete-orphan")


	def __init__(self, name, private, width, height, account_id):
		self.name = name
		self.private = private
		self.width = width
		self.height = height
		self.account_id = account_id
