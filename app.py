from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

#Register/Login Page
#Statuses: 'GET' - GET/plain open
#'reg_OK' - Register success, prompt login
#'login_OK' - Login success
#'reg_bad_char' - Username or password contained illegal char
#'reg_exists' - Account exists, prompt login
#'login_fail' - Login fail, prompt retry
@app.route("/")
@app.route("/auth/", methods=['GET', 'POST'])
def authenticate():
	if request.method == 'GET': #GET request
		return render_template('auth.html', status='GET')
		
	else: #POST request, form submission
		#Get the username & password entered
		entered_name = request.form['user']
		entered_pass = request.form['pass']
		
		if (request.form['auth_action'] == 'Register'): #Register attempt
			#Check that names are clean (no , or " or ' or backslash)
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
				#Successful login, show msg w/ username
				return render_template('auth.html', status='login_OK', uName=entered_name)
			else:
				#Failed login, prompt retry
				return render_template('auth.html', status='login_fail')

#is_input_clean(username, password)
#Returns false if either name contains , or " or ' or backslash
def is_input_clean(username, password):
	if (',' in username or '"' in username or "'" in username or "\\" in username
			or ',' in password or '"' in password or "'" in password or "\\" in password):
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
			user_store.close()
			return False #Account exists
			
	#Username is unique, proceed to store
	#TODO: In the future, salt before hashing!!! Better yet, use an hmac!
	user_store.write(username + ',' + hash256_dig(password))
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
			entry_pass = entry[len(username):]
			user_store.close()
			return entry_pass == hash256_dig(password)
			
	#No account found with this username
	user_store.close()
	return False
	
#hash256_dig
#returns hexdigest of sha256 hash of input
def hash256_dig(input):
	return hashlib.sha256(input).hexdigest()
	
	
app.debug = True #enable debugging
app.run()