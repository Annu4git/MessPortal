from flask import Flask, render_template, request, session
import model as model
import login as loginp
import json
import datetime
import sqlite3 as sql
from app import app

@app.route("/")
def login():
	return render_template("login.html")

@app.route("/authenticate", methods=['POST'])
def authenticate():
	msg={}
	print "authenticate 1"
	#test
	if 'username' in session:
		print session
		msg['roll_no'] = session['roll_no']
		msg['name'] = session['name']
		return render_template("dashboard.html", message=session['username'] +" has already logged in,  first logout!!!")
   	elif request.method == 'POST':
   		print "authenticate 2"
   		msg = loginp.authenticate_student(request)
   		
   		if msg['authenticate'] == False:
   			return render_template('login.html')
   		else:
   			print "authenticate 3"
	   		jso = json.dumps(msg)
	   		print "final json"
	   		print jso
                        print "broooooo" 
                        print msg["breakfast"][0]
			session['roll_no'] = msg['roll_no']
			session['name'] = msg['name']
			return render_template("dashboard.html", message=jso)

@app.route("/nextmonth", methods=['POST'])
def nextmonth(roll_no, month, year):
	msg={}
	print
	print
	print
	print


	print
	print
	print "in nextmonth"

	if request.method == 'POST':
   		print "authenticate 2"
   		msg = loginp.next_month(session['roll_no'], month, year)
   		msg["roll_no"]=session['roll_no']
		msg["name"]=session['name']
   		jso = json.dumps(msg)
   		print "final json"
   		print jso
   		return render_template("dashboard.html", message=jso)	

@app.route("/cancelmeals.html")
def cancelmeal():
	return render_template("cancel_meals.html")	

@app.route("/cancelmealstatus", methods=['POST'])
def cancelmealstatus():
         formdate=request.form['demo']
         datearr=formdate.split('-')
         starting_date=datearr[0]
         ending_date_space=datearr[1].split(' ')
         ending_date=ending_date_space[1]
         start_arr=starting_date.split('/')
         end_arr=ending_date.split('/')
         start_day=start_arr[0]
         start_month=start_arr[1]
         start_year=start_arr[2]
         end_day=end_arr[0]
         end_month=end_arr[1]
         end_year=end_arr[2]
         breakfast = request.form.get('meal_type_1')
         lunch = request.form.get('meal_type_2')
         dinner = request.form.get('meal_type_3')
	 msg={}
	 print "Hey there change_meal_status"
	 #try:

         meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
         bfast_data=meals["breakfast"]
	 lunch_data=meals["lunch"]
	 dinner_data=meals["dinner"]
	 with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			if breakfast:
                            query="UPDATE meal_registration SET bbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
			    cur.execute(query)
                            con.commit()
			if lunch:
                            query="UPDATE meal_registration SET lbit= '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
                            cur.execute(query)
                            con.commit()
			if dinner:
                            query="UPDATE meal_registration SET dbit= '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
                            cur.execute(query)
                            con.commit()                    
			    print "working"
	 
         return render_template("cancel_meals.html")
@app.route("/uncancelmealstatus", methods=['POST'])
def uncancelmealstatus():
         formdate=request.form['demo']
         datearr=formdate.split('-')
         starting_date=datearr[0]
         ending_date_space=datearr[1].split(' ')
         ending_date=ending_date_space[1]
         start_arr=starting_date.split('/')
         end_arr=ending_date.split('/')
         start_day=start_arr[0]
         start_month=start_arr[1]
         start_year=start_arr[2]
         end_day=end_arr[0]
         end_month=end_arr[1]
         end_year=end_arr[2]
         breakfast = request.form.get('meal_type_1')
         lunch = request.form.get('meal_type_2')
         dinner = request.form.get('meal_type_3')
	 msg={}
	 print "Hey there change_meal_status"
	 #try:

         meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
         bfast_data=meals["breakfast"]
	 lunch_data=meals["lunch"]
	 dinner_data=meals["dinner"]
	 with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			if breakfast:
                            query="UPDATE meal_registration SET bbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
			    cur.execute(query)
                            con.commit()
			if lunch:
                            query="UPDATE meal_registration SET lbit= '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
                            cur.execute(query)
                            con.commit()
			if dinner:
                            query="UPDATE meal_registration SET dbit= '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
                            cur.execute(query)
                            con.commit()                    
			    print "working"
	 
         return render_template("cancel_meals.html")
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
