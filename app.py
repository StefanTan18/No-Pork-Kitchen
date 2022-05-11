from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)

# hardcopy of the user data
user = "bob"
pswd = "bobby"
type = "customer"
name = "Stefan Tan"
address = "160 Convent Ave, New York, NY"
currentBalance = 50
warning = 2
isVIP = True

@app.route("/")
def home():
	if 'username' in session:
		if type == "customer":
			return render_template('customer.html', logged = True, username = session['username'])
		elif type == "chef":
			return render_template('chef.html', logged = True, username = session['username'])
		elif type == "delivery":
			return render_template('delivery.html', logged = True, username = session['username'])
	else:
		return render_template('guest.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
	try:
		username = request.form['username']
		password = request.form['password']

		if username == user and password == pswd:
			session['username'] = username
			return redirect(url_for('home'))
		else:
			flash("Wrong username or password!")
			return render_template('login.html')
	except:
		return render_template('login.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
	try:
		name = request.form['name']
		address = request.form['address']
		username = request.form['new_user']
		password = request.form['new_pswd']
		pswdCopy = request.form ['re_pswd']
		role = request.form['role']

		if password == pswdCopy:
			flash("Registration Complete! Please log in using your credentials.")
			return render_template('register.html')
		else:
			flash("Passwords do not match.")
			return render_template('register.html')
	
	except:
		return render_template('register.html')

@app.route("/profile", methods=['POST', 'GET'])
def profile():
	balance = 50 # test intial balance, balance = currentBalance gets UnboundLocalError: local variable 'currentBalance' referenced before assignment
	if 'username' in session:
		try:
			if type == 'customer':
				addedBalance = int(request.form['addedBalance'])
				if addedBalance > 0:
					balance += addedBalance
					currentBalance = balance
					return render_template('profile.html',
									isCustomer = True,
									VIP = isVIP,
									username = session['username'], 
									name = name,
									role = type, 
									address = address,
									warning = warning,
									balance = balance)
			else:
				return render_template('profile.html',
									isCustomer = False,
									VIP = False,
									username = session['username'],
									name = name,
									role = type, 
									address = address,
									warning = warning)

		except:
			if type == 'customer':
				return render_template('profile.html',
									isCustomer = True,
									VIP = isVIP,
									username = session['username'], 
									name = name,
									role = type, 
									address = address,
									warning = warning,
									balance = balance)
			else:
				return render_template('profile.html',
									isCustomer = False,
									VIP = False,
									username = session['username'],
									name = name,
									role = type, 
									address = address,
									warning = warning)

	else:
		return redirect(url_for('home'))


@app.route("/logout")
def logout():
	# removes stored data
	session.pop("username")
	
	return redirect(url_for("home"))

if __name__ == "__main__":
	app.secret_key = os.urandom(32)
	app.debug = True
	app.run()