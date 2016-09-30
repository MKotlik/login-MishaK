from Flask import flask, render_template, request

app = Flask(__name__)

username = "admin"
password = "123456"

@app.route("/")
def index():
	return "Index"

@app.route("/authenticate/")
def authenticate():
	if request.method == 'GET':
		return render_template('auth.html', status=0)
	else:
		if (request.form['user'] == 'admin' 
		and request.form['pass'] == '123456'):
			return render_template('auth.html', status=1)
		else:
			return render_template('auth.html', status=2)
	
app.debug = True #enable debugging
app.run()