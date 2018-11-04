import sqlite3 as sql

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
	print "Hey get_meal_registration for a student"
	try:

		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from meal_registration where roll_no=" + str(roll_no) 
			+ " and month=" + month + " and year=" + year
			cur.execute(query)

			print "here **"
			rows = cur.fetchall()
			for row in rows:
				print "row=",  row
			return rows
	except:
		print "connection fails"
		return "connection fails"

