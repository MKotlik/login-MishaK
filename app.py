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
		#Get the username & password entered
		entered_name = request.form['user']
		entered_pass = request.form['pass']
		
		if (request.form['auth_action'] == 'Register'): #Register attempt
			#Check that names are clean (no , or " or ')
			if not is_input_clean(entered_name, entered_pass):
				return render_template('auth.html', status='reg_bad_char')
			#Name is clean, proceed to register
			if register(entered_name, entered_pass) == True:
				#Account created successfully, promppt login
				return render_template('auth.html', status='reg_OK')
			else:
				#Account already exists, prompt login
				return render_template('auth.html', status='reg_exists')
				
		else: #Login attempt
			if login(entered_name, entered_pass) == True:
				#Successful login, show msg
				return render_template('auth.html', status='login_OK')
			else:
				#Failed login, prompt retry
				return render_template('auth.html', status='login_Fail')

#is_input_clean(username, password)
#Returns false if either name contains , or " or '
def is_input_clean(username, password):
	if (',' in username or '"' in username or "'" in username
			or ',' in password or '"' in password or "'" in password):
		return False; #input is dirty
	else:
		return True; #input is clean
			
#register(username, password)
#Statuses: False - account already exists
#True - registration successful
def register(username, password):
	#Open file in append mode for account checking/adding:
	user_store = open('data/user_store.csv', 'a')
	
	#Check uniqueness
	for entry in user_store:
		if entry.startswith(username):
			return False #Account exists
			
	#Username is unique, proceed to store
	#TODO: In the future, salt before hashing!!! Better yet, use an hmac!
	user_store.write(username + ',' + hashlib.sha256(password).hexdigest())
	user_store.close()
	return True #signify successful registration
	
#login(username, password)
#Statuses: False - no such account or password mismatch
#True - successfully authenticated
def login(username, password):
	#Open file in append mode for account checking:
	user_store = open('data/user_store.csv', 'r')
	
	for entry in user_store:
		if entry.startswith(username):
			#return whether given password matches given username
			return entry[len(username):] == hashlib.sha256(password).hexdigest()
			
	#No account found with this username
	return False
	
	
app.debug = True #enable debugging
app.run()