import sqlite3 as sql

def get_student_profile():
	print "Hey there"
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			cur.execute("select * from student_profile")
			rows = cur.fetchall()
			for row in rows:
				print "row=" +  row["name"]
			return rows
	except:
		print "connection fails"
		return "connection fails"