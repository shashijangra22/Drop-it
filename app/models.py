from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

viewers = db.Table('viewers',
		db.Column('file_id', db.Integer, db.ForeignKey('file.id')),
		db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
	)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(64))
	lname = db.Column(db.String(64))
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	pass_hash = db.Column(db.String(128))

	myFiles = db.relationship('File', backref='owner', lazy='dynamic')
	sharedFiles = db.relationship('File', secondary=viewers, backref=db.backref('viewers', lazy='dynamic'))
	
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
	isFile = db.Column(db.Boolean, default=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<File {}>'.format(self.filename)

