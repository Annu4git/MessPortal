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

				msg["roll_no"]=row[0]
				msg["name"]=row[1]
				msg["authenticate"]=True
				print "student_profile found"
				print "month & year : ", datetime.datetime.now().month, " : ", datetime.datetime.now().year
				meals = model.get_meal_registration_for_month(row[0], datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
	except:
		print "connection fails authenticate_student"
		msg["authenticate"]=False
	return msg

def next_month(roll_no, month, year):
	msg={}
	try:
		with sql.connect("mess_portal.db") as con:
			meals = model.get_meal_registration_for_month(roll_no, now.month, now.year)
			msg["breakfast"]=meals["breakfast"]
			msg["lunch"]=meals["lunch"]
			msg["dinner"]=meals["dinner"]
	except:
		print "connection fails authenticate_student"
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
