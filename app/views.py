from flask import render_template, request
import model

from app import app

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/studentprofile", methods = ['GET'])
def get_student_profile():
	if request.method == "GET":
		res = model.get_student_profile()
	return render_template("test.html", result = res, message = request.method)
