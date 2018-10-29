from app import app

@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/home.html')
def index():
	return "Welcome to Mess Portal"