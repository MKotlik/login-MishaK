from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/auth/", methods=['GET', 'POST'])
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