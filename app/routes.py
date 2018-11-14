from app import app, db, moment
from flask import render_template, session, url_for, redirect, request, send_from_directory
from app.models import User, File
from sqlalchemy import and_
from datetime import datetime
import os, shutil, json

def isLoggedIn():
	if 'userID' in session:
		user=User.query.get(session['userID'])
		if user:
			return True
	return False

@app.template_filter('getSize')
def getSize(item):
	user = User.query.get(session['userID'])
	base = app.config['UPLOADS']+"/"+user.username
	size=os.path.getsize(base+item.url+"/"+item.filename)
	return size

@app.route('/')
def index():
	if isLoggedIn():
		return redirect(url_for('home'))
	return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=='GET':
		return redirect(url_for('index'))
	username=request.form.get('usrname', False)
	if not username:
		return "Please fill username!"
	password=request.form.get('psswd', False)
	if not password:
		return "Please fill password!"
	user=User.query.filter_by(username=username).first()
	if user is None:
		return "Invalid Username!"
	if not user.check_pass(password):
		return "Invalid Password!"
	session['userID']=user.id
	return "1"

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method=='GET':
		return redirect(url_for('index'))
	fname=request.form.get('fname', False)
	if not fname:
		return "Please fill First Name!"
	lname=request.form.get('lname', False)
	if not lname:
		return "Please fill Last Name!"
	username=request.form.get('username', False)
	if not username:
		return "Please fill Username!"
	email=request.form.get('email', False)
	if not email:
		return "Please fill Email!"
	password=request.form.get('password', False)
	if not password:
		return "Please fill Password!"
	cpassword=request.form.get('confirmpassword', False)
	if not cpassword:
		return "Please fill Confirm Password!"
	if password!=cpassword:
		return "Passwords fields doesn't match!"
	user=User.query.filter_by(email=email).first()
	if user:
		return "Email already registered!"
	user=User.query.filter_by(username=username).first()
	if user:
		return "Username already exists!"
	user=User(fname=fname, lname=lname, username=username, email=email)
	user.set_pass(password)
	db.session.add(user)
	os.makedirs(app.config['UPLOADS']+"/" + username + "/home")
	db.session.commit()
	return "1"

@app.route('/editProfile', methods=['POST'])
def editProfile():
	fname=request.form.get('fname', False)
	if not fname:
		return "Please fill First Name!"
	lname=request.form.get('lname', False)
	if not lname:
		return "Please fill Last Name!"
	username=request.form.get('username', False)
	if not username:
		return "Please fill Username!"
	user=User.query.filter_by(username=username).first()
	if user:
		return "Username already exists!"
	user=User.query.get(session['userID'])
	user.fname=fname
	user.lname=lname
	os.chdir(app.config['UPLOADS'])
	os.rename(user.username,username)
	user.username=username
	db.session.commit()
	return "1"	

@app.route('/home/<path:path>')
def show(path):
	if isLoggedIn():
		path="/home/"+path
		path=path.replace(" ","%20")
		user=User.query.get(session['userID'])
		myFiles=File.query.filter(and_(File.owner==user, File.url==path, File.isFile==True))
		myFolders=File.query.filter(and_(File.owner==user, File.url==path, File.isFile==False))
		size=0
		for item in user.myFiles:
			size+=getSize(item)
		return render_template('home.html', user=user, myFiles=myFiles, spaceUsed=size, myFolders=myFolders, sharedFiles=user.sharedFiles)
	return redirect(url_for('index'))

@app.route('/home')
def home():
	if isLoggedIn():
		user=User.query.get(session['userID'])
		myFiles=File.query.filter(and_(File.owner==user, File.url=="/home", File.isFile==True))
		size=0
		for item in user.myFiles:
			size+=getSize(item)
		myFolders=File.query.filter(and_(File.owner==user, File.url=="/home", File.isFile==False))
		return render_template('home.html', user=user, myFiles=myFiles, spaceUsed=size, myFolders=myFolders, sharedFiles=user.sharedFiles)
	return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
	user=User.query.get(session['userID'])
	files = request.files.getlist("inputFiles")
	url=request.form.get('url', False)
	if len(files):
		for file in files:
			f=File.query.filter(and_(File.owner==user, File.url==url, File.isFile==True, File.filename==file.filename))
			if f.count():
				continue
			newFile=File(filename=file.filename, url=url, owner=user)
			db.session.add(newFile)
			path = app.config['UPLOADS'] + "/" + user.username + url
			file.save(os.path.join(path, file.filename))
	else:
		folderName=request.form.get('folderName', False)
		if len(folderName):
			newFolder=File(filename=folderName, url=url, owner=user, isFile=False)
			db.session.add(newFolder)
			try:
				os.mkdir(app.config['UPLOADS'] + "/" + user.username + url + "/" + folderName)
			except:
				return "Folder already exists!"
		else:
			return "Please enter name"
	db.session.commit()
	return "1"

@app.route('/share', methods=['POST'])
def share():
	fileID=request.form.get('fileID', False)
	file=File.query.get(fileID)
	if not file:
		return "File not found!"	# file not found
	username=request.form.get('username', False)
	if not username:
		return "Please fill a username!"	# user not found 
	toUser=User.query.filter_by(username=username).first()
	if not toUser:
		return "No such user exists!" #user not found
	toUser.sharedFiles.append(file)
	db.session.commit()
	return "File Successfully Shared with " + username

@app.route('/searchFiles', methods=['POST'])
def searchFiles():
	if isLoggedIn():
		user=User.query.get(session['userID'])
		searchText=request.form.get('filename',False)
		if not searchText:
			return "Enter something to search!"
		results=[]
		for item in user.myFiles:
			if item.isFile and searchText.lower() in str(item.filename).lower():
				results.append({"id":item.id,"filename":item.filename, "url":item.url ,"owner":item.owner.username})
		for item in user.sharedFiles:
			if item.isFile and searchText.lower() in str(item.filename).lower():
				results.append({"id":item.id,"filename":item.filename, "url":item.url, "owner":item.owner.username})
		return str(json.dumps(results))
	return "you are not logged in"

@app.route('/deleteFile/<fileID>')
def deleteFile(fileID):
	if isLoggedIn():
		user=User.query.get(session['userID'])
		file=File.query.get(fileID)
		if file:
			if file.owner.username==user.username:
				db.session.delete(file)
				if file.isFile:
					os.remove(os.path.join(app.config['UPLOADS'] + "/" + user.username + file.url, file.filename))
				else:
					path=file.url + "/" + file.filename
					children = File.query.filter(File.url.contains(path))
					for item in children:
						db.session.delete(item)
					shutil.rmtree(app.config['UPLOADS'] + "/" + user.username + path)
				db.session.commit()
				return file.filename + " Successfully Deleted!"
			else:
				return "you don't own this file"
		else:
			return "File not found!"
	return redirect(url_for('index'))


@app.route('/download/<int:fileID>')
def download_file(fileID):
	if isLoggedIn():
		file=File.query.get(fileID)
		path=app.config['UPLOADS']+"/"+file.owner.username+file.url
		return send_from_directory(path,file.filename, as_attachment=True)
	return redirect(url_for('index'))

@app.route('/view/<int:fileID>')
def view_file(fileID):
	if isLoggedIn():
		file=File.query.get(fileID)
		if file.isFile:
			path=app.config['UPLOADS']+"/"+file.owner.username+file.url
			return send_from_directory(path,file.filename)
	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session.pop('userID',None)
	return redirect(url_for('index'))

@app.errorhandler(404)
def http_404_handler(error):
	return redirect(url_for('index'))