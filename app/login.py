import sqlite3 as sql
from flask import session

def authenticate_student(request):
	msg={}
	print "Hey there authenticate_student"
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from student_profile where (email ='" + request.form['email'] + "' and password ='" + request.form['password'] + "')"
			cur.execute(query)
			row = cur.fetchone()
                        if(len(row)>0):
			   msg['roll_no']=row[0]
			   msg['name']=row[1]
	except:
		print "connection fails"
		return "connection fails"
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
