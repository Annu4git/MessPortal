from flask import Flask, render_template, request, session
import model as model
import login as loginp
import json
import datetime
import sqlite3 as sql
from flask import make_response
from app import app

@app.route("/")
def login():
	msg={}
	email = request.cookies.get('email')
	print "email : ", email
	print "session : ", session
	print "cookies : ", request.cookies
	if email in session:

		roll_no = session[email]
		msg["roll_no"] = roll_no
		
		name = request.cookies.get('name')
		msg["name"]=name
		msg["authenticate"]=True
		meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

		msg["breakfast"]=meals["breakfast"]
		msg["lunch"]=meals["lunch"]
		msg["dinner"]=meals["dinner"]
		msg["bcancel"]=meals["bcancel"]
		msg["lcancel"]=meals["lcancel"]
		msg["dcancel"]=meals["dcancel"]
		json_obj = json.dumps(msg)
		return render_template("dashboard.html", message=json_obj)
	else:
		return render_template("login.html")

@app.route("/logout")
def logout():
	email = request.cookies.get('email')
	session.pop(email,None)
	return render_template("login.html")

@app.route("/authenticate", methods=['POST'])
def authenticate():
	email = request.form['email']
	msg={}

	if request.method == 'POST':
			
			msg = loginp.authenticate_student(request)
			
			if msg['authenticate'] == False:
				return render_template('login.html')
			else:
				
				json_obj = json.dumps(msg)
				print "s11"
				print session
				session[email] = msg["roll_no"]
				session["name"] = msg["name"]
				session["roll_no"] = msg["roll_no"]
				roll_no=msg["roll_no"]
				now = datetime.datetime.now()
				print "s22"
				print session
				resp = make_response(render_template("dashboard.html", message=json_obj))
				resp.set_cookie('email', email)
				resp.set_cookie('name', msg["name"])

			return resp

@app.route("/nextmonth", methods=['POST'])
def nextmonth():
	msg={}
	email = request.cookies.get('email')
	print
	print
	print "**************************************"
	print "email : ", session[email]
	json_obj = request.form['mydata']
	json_data = json.loads(json_obj)
	print json_data['month']
	print json_data['year']
	print
	print
	print "in nextmonth"

	if request.method == 'POST':
		
		msg = loginp.next_month(session['roll_no'], int(json_data['month'])+1, int(json_data['year']))
		jso = json.dumps(msg)
		return jso

@app.route("/getmessmenu", methods=['POST'])
def get_mess_menu():
	msg={}
	email = request.cookies.get('email')
	print
	print
	print "**************************************"
	print "email : ", session[email]
	json_obj = request.form['mydata_mess_menu']
	json_data = json.loads(json_obj)
	breakfast = json_data['breakfast']
	lunch = json_data['lunch']
	dinner = json_data['dinner']
	day = json_data['day']
	print "in get_mess_menu"
	print day
	if request.method == 'POST':
		
		msg = model.get_mess_menu(breakfast, lunch, dinner, day)
		jso = json.dumps(msg)
		return jso

@app.route("/getmealmenu", methods=['POST'])
def get_meal_menu():
	print "getmealmenu"
	msg={}
	email = request.cookies.get('email')
	print
	print
	print "**************************************"
	print "email : ", session[email]
	json_obj = request.form['mydata_mess_menu']
	json_data = json.loads(json_obj)
	meal = json_data['meal']
	day = json_data['day']
	print "in get_meal_menu"
	print day
	if request.method == 'POST':
		
		msg = model.get_meal_menu(meal, day)
		jso = json.dumps(msg)
		return jso


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

@app.route("/cancelcurrbreakfast", methods=['POST'])
def cancelcurrbreakfast():
				now = datetime.datetime.now()
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals["bcancel"][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET bbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET bbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						cur.execute(query)
						con.commit()
				msg={}
				email = request.cookies.get('email')
				print "email : ", email
				print "session : ", session
				print "cookies : ", request.cookies

				roll_no = session[email]
				msg["roll_no"] = roll_no

				name = request.cookies.get('name')
				msg["name"]=name
				msg["authenticate"]=True
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
				msg["bcancel"]=meals["bcancel"]
				msg["lcancel"]=meals["lcancel"]
				msg["dcancel"]=meals["dcancel"]
				json_obj = json.dumps(msg)
				return render_template("dashboard.html", message=json_obj)

@app.route("/cancelcurrlunch", methods=['POST'])
def cancelcurrlunch():
				now = datetime.datetime.now()
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals["lcancel"][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET lbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET lbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						cur.execute(query)
						con.commit()
				msg={}
				email = request.cookies.get('email')
				print "email : ", email
				print "session : ", session
				print "cookies : ", request.cookies

				roll_no = session[email]
				msg["roll_no"] = roll_no

				name = request.cookies.get('name')
				msg["name"]=name
				msg["authenticate"]=True
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
				msg["bcancel"]=meals["bcancel"]
				msg["lcancel"]=meals["lcancel"]
				msg["dcancel"]=meals["dcancel"]
				json_obj = json.dumps(msg)
				return render_template("dashboard.html", message=json_obj)

@app.route("/cancelcurrdinner", methods=['POST'])
def cancelcurrdinner():
				now = datetime.datetime.now()
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals["dcancel"][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET dbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET dbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						cur.execute(query)
						con.commit()
				msg={}
				email = request.cookies.get('email')
				print "email : ", email
				print "session : ", session
				print "cookies : ", request.cookies

				roll_no = session[email]
				msg["roll_no"] = roll_no

				name = request.cookies.get('name')
				msg["name"]=name
				msg["authenticate"]=True
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
				msg["bcancel"]=meals["bcancel"]
				msg["lcancel"]=meals["lcancel"]
				msg["dcancel"]=meals["dcancel"]
				json_obj = json.dumps(msg)
				return render_template("dashboard.html", message=json_obj)

@app.route("/change_mess_registration.html")
def change_mess_registration():
	return render_template("change_mess_registration.html")	

@app.route("/default_mess.html")
def default_mess():
	return render_template("default_mess.html")	

@app.route("/dashboard.html")
def show_dashboard():
	msg={}
	email = request.cookies.get('email')
	if email in session:

		roll_no = session[email]
		msg["roll_no"] = roll_no
		
		name = request.cookies.get('name')
		msg["name"]=name
		msg["authenticate"]=True
		meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

		msg["breakfast"]=meals["breakfast"]
		msg["lunch"]=meals["lunch"]
		msg["dinner"]=meals["dinner"]
		msg["bcancel"]=meals["bcancel"]
		msg["lcancel"]=meals["lcancel"]
		msg["dcancel"]=meals["dcancel"]
		json_obj = json.dumps(msg)
		return render_template("dashboard.html", message=json_obj)
	else:
		return render_template("login.html")	



@app.route("/change_mess_menu.html")
def show_change_mess_menu():
	return render_template("change_mess_menu.html")	

@app.route("/changemenu", methods=['POST'])
def change_menu():
	msg={}
	
	mess = request.form['mess']+"_menu";
	day = request.form['day']
	meal = request.form['meal']
	newmenu = request.form['newmenu']
	
	msg["mess"]=mess
	msg["day"]=day;
	msg["meal"]=meal;
	msg["newmenu"]=newmenu;
	json_obj=json.dumps(msg)

	model.change_menu(mess,day,meal,newmenu)
	return render_template("change_mess_menu.html",status=1)

@app.route("/change_default_mess_admin.html")
def show_change_default_mess_admin():
	return render_template("change_default_mess_admin.html")	

@app.route("/change_default_mess", methods=['POST'])
def change_default_mess():
	msg={}
	
	student_rollno = request.form['student_rollno'];
	default_breakfast_mess = request.form['default_breakfast_mess']
	default_lunch_mess = request.form['default_lunch_mess']
	default_dinner_mess = request.form['default_dinner_mess']
	
	model.change_default_mess(student_rollno,default_breakfast_mess,default_lunch_mess,default_dinner_mess)
	return render_template("change_default_mess_admin.html",status=1)



