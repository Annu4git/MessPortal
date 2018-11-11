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

