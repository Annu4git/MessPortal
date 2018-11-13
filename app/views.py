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

@app.route("/admin")
def login_admin():
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
		json_obj = json.dumps(msg)
		return render_template("dashboard.html", message=json_obj)
	else:
		return render_template("login_admin.html")

@app.route("/logout")
def logout():
	email = request.cookies.get('email')
	session.pop(email,None)
	session.pop("name",None)
	session.pop("roll_no",None)
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
				
				session[email] = msg["roll_no"]
				session["name"] = msg["name"]
				session["roll_no"] = msg["roll_no"]
				session["user"] = "student"
				roll_no=msg["roll_no"]

				if msg["first_login"] == True:
					resp = make_response(render_template("set_default_mess.html", message=json_obj))
				else:
					resp = make_response(render_template("dashboard.html", message=json_obj))

				resp.set_cookie('email', email)
				resp.set_cookie('name', msg["name"])

			return resp

@app.route("/authenticate_admin", methods=['POST'])
def authenticate_admin():
	email = request.form['email']
	msg={}

	if request.method == 'POST':
			
			msg = loginp.authenticate_admin(request)
			
			if msg['authenticate'] == False:
				return render_template('login.html')
			else:
				
				json_obj = json.dumps(msg)
				
				session[email] = msg["admin_id"]
				session["name"] = msg["name"]
				session["user"] = "admin"
				
				resp = make_response(render_template("empty.html", message=json_obj))

				resp.set_cookie('email', email)
				resp.set_cookie('name', msg["name"])

			return resp

@app.route("/firstlogin", methods=['POST'])
def first_login():

	if not session.get('name'):
		return render_template('login.html')

	email = request.form['email']
	msg={}

	if request.method == 'POST':
			msg = loginp.authenticate_student(request)
			
			if msg['authenticate'] == False:
				return render_template('login.html')
			else:
				
				json_obj = json.dumps(msg)
				
				session[email] = msg["roll_no"]
				session["name"] = msg["name"]
				session["roll_no"] = msg["roll_no"]
				roll_no=msg["roll_no"]

				if msg["first_login"] == True:
					resp = make_response(render_template("set_default_mess.html", message=json_obj))
				else:
					resp = make_response(render_template("dashboard.html", message=json_obj))

				resp.set_cookie('email', email)
				resp.set_cookie('name', msg["name"])

	#return resp
	return ""

@app.route("/nextmonth", methods=['POST'])
def nextmonth():
	msg={}
	email = request.cookies.get('email')
	json_obj = request.form['mydata']
	json_data = json.loads(json_obj)

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
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
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
# @app.route("/home.html")
# def index():
# 	return render_template("index.html")

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



@app.route("/cancelcurrI", methods=['POST'])
def cancelcurrI():
				now = datetime.datetime.now()
				hours=now.hour
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
                
				if(hours>=22 and hours<=23):
					start_day+=1
					end_day+=1
					mybit="bbit"
					checkcancel="bcancel"

				if(hours>=0 and hours<=9):
				     mybit="bbit" 
				     checkcancel="bcancel"

				if(hours>=10 and hours<=14):
				     mybit="lbit"
				     checkcancel="lcancel"   

				if(hours>=15 and hours<=21):
				   mybit="dbit"
				   checkcancel="dcancel"

				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals[checkcancel][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET "+mybit+" = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET "+mybit+" = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
					
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

@app.route("/cancelcurrII", methods=['POST'])
def cancelcurrII():
				now = datetime.datetime.now()
				hours=now.hour
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
				if(hours>=22 and hours<=23):
					start_day+=1
					end_day+=1
					mybit="lbit"
					checkcancel="lcancel"

				if(hours>=0 and hours<=9):
				    mybit="lbit"
				    checkcancel="lcancel"

				if(hours>=10 and hours<=14):
				    mybit="dbit"
				    checkcancel="dcancel"   

				if(hours>=15 and hours<=21):
					start_day+=1
					end_day+=1
					mybit="bbit"
					checkcancel="bcancel"
				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals[checkcancel][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET "+mybit+" = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET "+mybit+" = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
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

@app.route("/cancelcurrIII", methods=['POST'])
def cancelcurrIII():
				now = datetime.datetime.now()
				hours=now.hour
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
				if(hours>=22 and hours<=23):
					start_day+=1
					end_day+=1
					mybit="dbit"
					checkcancel="dcancel"

				if(hours>=0 and hours<=9):
				    mybit="dbit"
				    checkcancel="dcancel"

				if(hours>=10 and hours<=14):
					start_day+=1
					end_day+=1
					mybit="bbit"
					checkcancel="bcancel"  

				if(hours>=15 and hours<=21):
					start_day+=1
					end_day+=1
					mybit="lbit"
					checkcancel="lcancel"
				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals[checkcancel][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET "+mybit+" = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET "+mybit+" = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
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
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	return render_template("change_mess_registration.html")	

@app.route("/default_mess.html")
def default_mess():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	return render_template("default_mess.html")	

@app.route("/dashboard.html")
def show_dashboard():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
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
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
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
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
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


@app.route("/datewisemesschange", methods=['POST'])
def datewisemesschange():
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
		messname1=request.form['messname']
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			if breakfast:
											query="UPDATE meal_registration SET bbit ='0',breakfast = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											print query
											cur.execute(query)
											con.commit()
			if lunch:
											query="UPDATE meal_registration SET lbit ='0',lunch = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()
			if dinner:
											query="UPDATE meal_registration SET dbit ='0',dinner = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
											cur.execute(query)
											con.commit()                    

		return render_template("change_mess_registration.html")

@app.route("/cancelmealdaywise", methods=['POST'])
def cancelmealdaywise():
			now = datetime.datetime.now()
			start_day=now.day
			start_month=now.month
			start_year=now.year
			end_day=31
			end_month=now.month
			end_year=now.year					
			daycancel=request.form['cancelday']
			breakfast = request.form.get('meal_type_1')
			lunch = request.form.get('meal_type_2')
			dinner = request.form.get('meal_type_3')
			with sql.connect("mess_portal.db") as con:
					con.row_factory = sql.Row
					cur = con.cursor()
					if breakfast:
												query="UPDATE meal_registration SET bbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												print query
												cur.execute(query)
												con.commit()
					if lunch:
												query="UPDATE meal_registration SET lbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												con.commit()
					if dinner:
												query="UPDATE meal_registration SET dbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												con.commit()                    
														

			return render_template("cancel_meals.html")

@app.route("/uncancelmealdaywise", methods=['POST'])
def uncancelmealdaywise():
			now = datetime.datetime.now()
			start_day=now.day
			start_month=now.month
			start_year=now.year
			end_day=31
			end_month=now.month
			end_year=now.year					
			daycancel=request.form['cancelday']
			breakfast = request.form.get('meal_type_1')
			lunch = request.form.get('meal_type_2')
			dinner = request.form.get('meal_type_3')
			with sql.connect("mess_portal.db") as con:
					con.row_factory = sql.Row
					cur = con.cursor()
					if breakfast:
												query="UPDATE meal_registration SET bbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												print query
												cur.execute(query)
												con.commit()
					if lunch:
												query="UPDATE meal_registration SET lbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												con.commit()
					if dinner:
												query="UPDATE meal_registration SET dbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												con.commit()                    
														

			return render_template("cancel_meals.html")			

@app.route("/daywisemesschange", methods=['POST'])
def daywisemesschange():
		now = datetime.datetime.now()
		start_day=now.day
		start_month=now.month
		start_year=now.year
		end_day=31
		end_month=now.month
		end_year=now.year					
		daychange=request.form['changeday']
		breakfast = request.form.get('meal_type_1')
		lunch = request.form.get('meal_type_2')
		dinner = request.form.get('meal_type_3')
		messname1=request.form['messname1']
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			if breakfast:
											query="UPDATE meal_registration SET bbit ='0',breakfast = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daychange)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											
											cur.execute(query)
											con.commit()
			if lunch:
											query="UPDATE meal_registration SET lbit ='0',lunch = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daychange)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()
			if dinner:
											query="UPDATE meal_registration SET dbit ='0',dinner = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daychange)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
											cur.execute(query)
											con.commit()                    

		return render_template("change_mess_registration.html")

@app.route("/generate_mess_report.html")
def show_generate_report():
	return render_template("generate_mess_report.html")


@app.route("/generatereport",methods=['POST'])
def generatereport():
	msg={}
	name_of_mess=request.form['name_of_mess']
	report_date=request.form['report_date']

	report_date=report_date.split("-")

	day=report_date[2]
	month=report_date[1]
	year=report_date[0]

	bdata,ldata,ddata=model.generatereport(name_of_mess,day,month,year)

	msg["breakfast_list"]=(bdata)
	msg["lunch_list"]=(ldata)
	msg["dinner_list"]=(ddata)
	msg["mess"]=name_of_mess
	msg["date"]=day+"/"+month+"/"+year
	json_obj = json.dumps(msg)
	return render_template("display_report_data.html", message=json_obj)

@app.route("/mess_registration_stats.html")
def show_mess_registration_stats():
	return render_template("/mess_registration_stats.html")

@app.route("/showmessstats")
def messstats():
	msg={}
	

	data=model.messstats()

	# msg["breakfast_list"]=(bdata)
	# msg["lunch_list"]=(ldata)
	# msg["dinner_list"]=(ddata)
	# msg["mess"]=name_of_mess
	# msg["date"]=day+"/"+month+"/"+year
	# json_obj = json.dumps(msg)
	# return render_template("display_report_data.html", message=json_obj)


	return "Hello"#render_template("/mess_registration_stats.html")

@app.route("/admin_dashboard.html")
def show_admin_dashboard():
	return render_template("/admin_dashboard.html")

@app.route("/logout.html")
def show_logout_page():
	return render_template("/logout.html")

@app.route("/login.html")
def show_login_page():
	return render_template("/login.html")
