from flask import Flask, render_template, request, session, redirect, url_for
import os
import hashlib

app= Flask(__name__)

#Config from config.py
app.config.from_object('config')

#Index/Welcome page
#Sent here by default or when logged in
@app.route("/")
def index():
    #Check if user logged in
    if 'username' in session:
        return render_template('index.html', user=session['username'])
    else:
        return redirect(url_for('authenticate'))

#Register/Login Page
#Statuses: 'GET' - GET/plain open
#'reg_OK' - Register success, prompt login
#'login_OK' - Login success
#'reg_bad_char' - Username or password contained illegal char
#'reg_exists' - Account exists, prompt login
#'login_fail' - Login fail, prompt retry
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
				#Successful login, send to index.html
				return redirect(url_for('index'))
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
	user_store = open('data/user_store.csv', 'a+')
	
	#Check uniqueness
	for entry in user_store:
		if entry.startswith(username):
			user_store.close()
			return False #Account exists
			
	#Username is unique, proceed to store
	#TODO: In the future, salt before hashing!!! Better yet, use an hmac!
	
	#DEBUG: print "Register: " + password
	#DEBUG: print "Hashed register: " + hash256_dig(password)
	
	user_store.write(username + ',' + hash256_dig(password) + '\n')
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
			entry_pass = entry[len(username)+1:-1]
			
			#DEBUG: print entry_pass
			#DEBUG: print hash256_dig(password)
			
			user_store.close()
			
			#DEBUG: print entry_pass == hash256_dig(password)
			
			if entry_pass == hash256_dig(password):
                session['username'] = username #log user into session
                return True
            return False #password doesn't match
			
	#No account found with this username
	user_store.close()
	return False
	
#hash256_dig
#returns hexdigest of sha256 hash of input
def hash256_dig(input):
	return hashlib.sha256(input).hexdigest()
	
	
app.debug = True #enable debugging
app.run()
