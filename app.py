from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

#Register/Login Page
#Statuses: 'GET' - GET/plain open
#'reg_OK' - Register success, prompt login
#'login_OK' - Login success
#'reg_bad_char' - Username or password contained illegal char
#'reg_exists' - Account exists, prompt login
#'login_Fail' - Login fail, prompt retry
@app.route("/auth/", methods=['GET', 'POST'])
def authenticate():
	if request.method == 'GET': #GET request
		return render_template('auth.html', status='GET')
	else: #POST request, form submission
		if (request.form['auth_action'] == 'Register'): #Register attempt
			#Check that names are clean (no , or " or ')
			#Call register() func to ensure uniqueness and register
		else: #Assume login
			#Do login procedure here
		if (request.form['user'] == 'admin' 
		and request.form['pass'] == '123456'):
			return render_template('auth.html', status=1)
		else:
			return render_template('auth.html', status=2)

#is_input_clean(username, password)
#Returns false if either name contains , or " or '
def is_input_clean(username, password):
	if (',' in username or '"' in username or "'" in username
			or ',' in password or '"' in password or "'" in password):
		return False; #input is dirty
	else:
		return True; #input is clean
			
#register(username, password)
#Statuses: 'exists' - account already exists
#'OK' - registration successful
def register(username, password):
	#Open file in append mode for account checking/adding:
	user_store = open('data/user_store.csv', 'a')
	
	#Check uniqueness
	for entry in user_store:
		if entry.startswith(username):
			return 'exists' #Account exists
			
	#Username is unique, proceed to store
	#TODO: In the future, salt before hashing!!! Better yet, use an hmac!
	user_store.write(username + ',' + hashlib.sha256(password).hexdigest())
	user_store.close()
	return 'OK' #signify successful registration
	
app.debug = True #enable debugging
app.run()