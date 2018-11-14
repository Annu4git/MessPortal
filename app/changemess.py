import sqlite3 as sql
import datetime

def daywisemesschange(roll_no, meal, mess, day):

	now = datetime.datetime.now()
	start_day=now.day
	start_month=now.month
	start_year=now.year
	end_day=start_day+7
	end_month=now.month
	end_year=now.year					
	
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			print "fineee"
			query="UPDATE meal_registration SET bbit ='0'," + meal + " = "+"'"+ mess +"'"+" WHERE (roll_no="+str(roll_no)+" and dayname="+"'"+str(day)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
			print query
			cur.execute(query)
			con.commit()
	except:
		print "wwweee error"