from app import app, db
from flask import render_template, session, url_for, redirect, request
from app.models import User, File
from sqlalchemy import and_
import json

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

@app.route('/home/<path:path>')
def show(path):
	if isLoggedIn():
		path="/home/"+path
		path=path.replace(" ","%20")
		user=User.query.get(session['userID'])
		myFiles=File.query.filter(and_(File.owner==user, File.url==path))
		sharedWith={}
		for item in myFiles:
			sharedWith[item.id]=[]
			viewers=json.loads(item.viewers)
			for u in viewers:
				sharedWith[item.id].append(u)
		return render_template('home.html', user=user, sharedWith=sharedWith, myFiles=myFiles)
	return redirect(url_for('index'))

@app.route('/home')
def home():
	if isLoggedIn():
		user=User.query.get(session['userID'])
		AllFiles=File.query.all()
		sharedFiles=[]
		for item in AllFiles:
			viewers=json.loads(item.viewers)
			if user.username in viewers:
				sharedFiles.append(item)
		myFiles=File.query.filter(and_(File.owner==user, File.url=="/home"))
		sharedWith={}
		for item in myFiles:
			sharedWith[item.id]=[]
			viewers=json.loads(item.viewers)
			for u in viewers:
				sharedWith[item.id].append(u)
		return render_template('home.html', user=user, sharedWith=sharedWith, myFiles=myFiles, sharedFiles=sharedFiles)
	return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
	user=User.query.get(session['userID'])
	file = request.files.get('inputFile', False)
	url=request.form.get('url', False)
	if file:
		newFile=File(filename=file.filename, url=url, data=file.read(), owner=user)
		db.session.add(newFile)
	else:
		folderName=request.form['folderName']
		newFolder=File(filename=folderName, url=url, owner=user, isFile=False)
		db.session.add(newFolder)
	db.session.commit()
	return "1"

@app.route('/share', methods=['POST'])
def share():
	fileID=request.form.get('fileID', False)
	file=File.query.get(fileID)
	if not file:
		return "1"	# file not found
	username=request.form.get('username', False)
	if not username:
		return "2"	# user not found 
	toUser=User.query.filter_by(username=username)
	if not toUser:
		return "2" #user not found
	viewers=json.loads(file.viewers)
	viewers[username]=True
	file.viewers=json.dumps(viewers)
	db.session.commit()
	return "3"

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