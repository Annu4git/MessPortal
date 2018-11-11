import sqlite3 as sql
import datetime

def get_meal_registration_for_today(roll_no, day, month, year):
	print "Hey get_meal_registration for a student"
	try:

		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from meal_registration where roll_no=" + str(roll_no) 
			+ " and day=" + day + " and month=" + month + " and year=" + year
			cur.execute(query)
			print "here **"
			rows = cur.fetchall()
			for row in rows:
				print "row=",  row
			return rows
	except:
		print "connection fails"
		return "connection fails"

def get_meal_registration_for_month(roll_no, month, year):
	print "Hey get_meal_registration for a student for month"
	try:

		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			print "roll_no : ", roll_no
			
			query="select * from meal_registration where roll_no=" + str(roll_no) + " and month=" + str(month) + " and year=" + str(year)
			
			cur.execute(query)
			
			rows = cur.fetchall()
			breakfast = {}
			lunch = {}
			dinner = {}
			bcancel = {}
			lcancel = {}
			dcancel = {}
			i=0
			obj={}
			print "printing rows"
			for row in rows:

				breakfast[i]=row[4]
				lunch[i]=row[5]
				dinner[i]=row[6]
				bcancel[i]=row[7]
				lcancel[i]=row[8]
				dcancel[i]=row[9]
				i=i+1
			obj["breakfast"]=breakfast
			obj["lunch"]=lunch
			obj["dinner"]=dinner
			obj["bcancel"]=bcancel
			obj["lcancel"]=lcancel
			obj["dcancel"]=dcancel
			return obj
	except:
		print "connection fails get_meal_registration_for_month"
		return "connection fails get_meal_registration_for_month"

def get_mess_menu(breakfast, lunch, dinner, day):

	print "inside model get_mess_menu"
	menu={}

	breakfast = breakfast.lower()
	lunch = lunch.lower()
	dinner = dinner.lower()

	print breakfast
	print lunch
	print dinner
	print day

	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select breakfast from " + breakfast + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["breakfast_menu"] = rows[0][0]

			query="select lunch from " + lunch + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["lunch_menu"] = rows[0][0]

			query="select dinner from " + dinner + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["dinner_menu"] = rows[0][0]

	except:
		print "connection fails get_mess_menu"
		return "connection fails get_mess_menu"
	return menu

def get_meal_menu(meal, day):

	print "inside model get_mess_menu"
	menu={}

	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()

			date = datetime.datetime.now().day
			month = datetime.datetime.now().month
			year = datetime.datetime.now().year
			print "this query"
			query="select "+ meal +" from  meal_registration where day=" + str(date) + " and month=" + str(month) + " and year=" + str(year)
			
			print query
			cur.execute(query)
			rows = cur.fetchall()
			mess = rows[0][0]
			print mess

			query="select "+ meal +" from " + mess + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["meal_menu"] = rows[0][0]
			menu["mess"] = mess
			print menu

	except:
		print "connection fails get_mess_menu"
		return "connection fails get_mess_menu"
	return menu
