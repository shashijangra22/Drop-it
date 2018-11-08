from app import app, db
from flask import render_template, session, url_for, redirect, request
from app.models import User, File

def isLoggedIn():
	if 'userID' in session:
		return True
	return False

@app.route('/')
def index():
	if isLoggedIn():
		return redirect(url_for('home'))
	return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=='GET':
		return redirect(url_for('index'))
	username=request.form['username']
	password=request.form['password']
	user=User.query.filter_by(username=username).first()
	if user is None or not user.check_pass(password):
		return "invalid details!"
	session['userID']=user.id
	return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method=='GET':
		return redirect(url_for('index'))
	username=request.form['username']
	password=request.form['password']
	email=request.form['email']
	user=User.query.filter_by(email=email).first()
	if user:
		return "Email already registered!"
	user=User.query.filter_by(username=username).first()
	if user:
		return "Username already exists!"
	user=User(username=username, email=email)
	user.set_pass(password)
	db.session.add(user)
	db.session.commit()
	return "successful registration!"

@app.route('/home')
def home():
	if isLoggedIn():
		user=User.query.get(session['userID'])
		return render_template('home.html', user=user)
	return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
	user=User.query.get(session['userID'])
	file = request.files['inputFile']
	newFile=File(filename=file.filename, data=file.read(), owner=user)
	db.session.add(newFile)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/deleteFile/<fileID>')
def deleteFile(fileID):
	file=File.query.get(fileID)
	db.session.delete(file)
	db.session.commit()
	return "successfully deleted"

@app.route('/logout')
def logout():
	session.pop('userID',None)
	return redirect(url_for('index'))

@app.errorhandler(404)
def http_404_handler(error):
	return redirect(url_for('index'))