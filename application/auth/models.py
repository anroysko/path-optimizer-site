from application import db, bcrypt

def check_password(password_hash, plaintext):
	return bcrypt.check_password_hash(password_hash, plaintext)

def encrypt_password(plaintext):
	return bcrypt.generate_password_hash(plaintext, rounds=6).decode('utf-8')

class User(db.Model):
	__tablename__ = "account"

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	username = db.Column(db.String(144), nullable=False)
	_password = db.Column(db.String(144), nullable=False) # Hashed

	perms = db.relationship("Perm", backref='account', lazy=True, cascade="all, delete-orphan")

	def __init__(self, username, password):
		self.username = username
		self._password = encrypt_password(password)

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True
