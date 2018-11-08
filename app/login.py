import sqlite3 as sql
import json
import model
import datetime
from flask import session


def authenticate_student(request):

	msg={}
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from student_profile where (email ='" + request.form['email'] + "' and password ='" + request.form['password'] + "')"
			cur.execute(query)
			print cur
			row = cur.fetchone()
			if(len(row)>0):
				roll_no = row[0]

				msg["roll_no"]=roll_no
				msg["name"]=row[1]
				msg["authenticate"]=True
				
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
                msg["bcancel"]=meals["bcancel"]
                msg["lcancel"]=meals["lcancel"]
                msg["dcancel"]=meals["dcancel"]
	except:
		print "connection fails authenticate_student"
		msg["authenticate"]=False
	return msg

def next_month(roll_no, month, year):
	msg={}
	try:
		with sql.connect("mess_portal.db") as con:
			meals = model.get_meal_registration_for_month(roll_no, month, year)
			msg["breakfast"]=meals["breakfast"]
			msg["lunch"]=meals["lunch"]
			msg["dinner"]=meals["dinner"]
			msg["bcancel"]=meals["bcancel"]
			msg["lcancel"]=meals["lcancel"]
			msg["dcancel"]=meals["dcancel"]
	except:
		print "connection fails next_month"
		msg["authenticate"]=False
	return msg

def authenticate_admin(request):
	print "Hey there"
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from admin_profile where (admin_id =" + request.form['admin_id'] + " and password ='" + request.form['password'] + "')"
			cur.execute(query)
			rows = cur.fetchall()
			print "size : ", len(rows)
			for row in rows:
				print "row=", row
			return rows
	except:
		print "connection fails"
		return "connection fails"
