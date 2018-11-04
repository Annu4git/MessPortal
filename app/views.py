from flask import Flask, render_template, request, session
import model as model
import login as loginp

from app import app

@app.route("/")
def login():
	return render_template("login.html")

@app.route("/authenticate", methods=['POST'])
def authenticate():
	msg={}
	print "authenticate 1"

	if 'username' in session:
		print session
		msg['roll_no'] = session['roll_no']
		msg['name'] = session['name']
		return render_template("dashboard.html", message=session['username'] +" has already logged in,  first logout!!!")
   	elif request.method == 'POST':
   		print "authenticate 2"
   		msg = loginp.authenticate_student(request)
   		print "bool : ",bool(msg)
   		if bool(msg) is False:
   			print "login failed"
   		else:
   			print "authenticate 3"
			session['roll_no'] = msg['roll_no']
			session['name'] = msg['name']
			print "successful login"

	return render_template("dashboard.html", message=msg)

	return render_template('login.html')


@app.route("/home.html")
def index():
	return render_template("index.html")

@app.route("/studentprofile", methods = ['GET'])
def get_student_profile():
	if request.method == "GET":
		res = model.get_student_profile(2018201022)
	return render_template("test.html", result = res, message = request.method)

@app.route("/mealregistration", methods = ['GET'])
def get_meal_registration():
	if request.method == "GET":
		res = model.get_meal_registration()
	return render_template("test.html", result = res, message = request.method)
