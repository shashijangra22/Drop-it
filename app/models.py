from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	pass_hash = db.Column(db.String(128))

	files = db.relationship('File', backref='owner', lazy='dynamic')

	def set_pass(self, password):
		self.pass_hash=generate_password_hash(password)

	def check_pass(self,password):
		return check_password_hash(self.pass_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(120))
	url = db.Column(db.String(120))
	data = db.Column(db.LargeBinary)
	isFile = db.Column(db.Boolean, default=True)
	viewers = db.Column(db.Text, default="{}")
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<File {}>'.format(self.filename)