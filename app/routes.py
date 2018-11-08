from app import app, db
from flask import render_template, session, url_for, redirect, request
from app.models import User, File

def isLoggedIn():
	if 'username' in session:
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
	session['username']=username
	return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method=='GET':
		return redirect(url_for('index'))
	username=request.form['username']
	password=request.form['password']
	email=request.form['email']
	user=User.query.filter_by(username=username).first()
	if user is not None:
		return "User already exists!"
	user=User(username=username, email=email)
	user.set_pass(password)
	db.session.add(user)
	db.session.commit()
	return "successful registration!"

@app.route('/home')
def home():
	if isLoggedIn():
		return render_template('home.html', username=session['username'])
	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect(url_for('index'))

@app.errorhandler(404)
def http_404_handler(error):
	return redirect(url_for('index'))