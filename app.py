from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

# from flaskext.mysql import MySQL

# import backend

app = Flask(__name__)
# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '5326atAT!'
# app.config['MYSQL_DATABASE_DB'] = 'noporkkitchendb'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# hardcopy of the user data
userid = 1
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
			return render_template('customer.html',
									logged = True, 
									username = session['username'])
		elif type == "chef":
			menu = ["Pizza", "Sushi"]
			return render_template('chef.html', 
									logged = True, 
									username = session['username'],
									foods = menu)
		elif type == "delivery":
			orders = ["Order #1", "Order #2"]
			return render_template('delivery.html',
									logged = True, 
									username = session['username'],
									orders = orders)
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
			try:
				# print('Hello')
				# backend.registerSQL(userid, name, address, username, password, role)
				# print('Bye')
				# userid = userid + 1
				flash("Registration Complete! Please log in using your credentials.")
				return render_template('register.html')
			except:
				flash("Registration Failed.")
				return render_template('register.html')
		else:
			flash("Passwords do not match.")
			return render_template('register.html')
	
	except:
		return render_template('register.html')

@app.route("/profile", methods=['POST', 'GET'])
def profile():
	balance = 50 # test intial balance, balance = currentBalance gets UnboundLocalError: local variable 'currentBalance' referenced before assignment
	orders = ['ORDER1', "ORDER2", "ORDER3"]
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
									orders = orders,
									balance = balance)
			else:
				return render_template('profile.html',
									isCustomer = False,
									VIP = False,
									username = session['username'],
									name = name,
									role = type, 
									address = address,
									warning = warning,
									orders = orders)

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
									orders = orders,
									balance = balance)
			else:
				return render_template('profile.html',
									isCustomer = False,
									VIP = False,
									username = session['username'],
									name = name,
									role = type, 
									address = address,
									warning = warning,
									orders = orders)

	else:
		return redirect(url_for('home'))

@app.route("/food/<food>")
def food(food):
	#food = "Pizza"
	chef = "Jack"
	price = 5
	rating = 4
	names = ["John Smith", "Danny Watson", "Willy Wonka"]
	description = "Lorem ipsum dolor sit, amet consectetur adipisicing elit.  Accusamus numquam assumenda hic aliquam vero sequi velit molestias doloremque molestiae dicta?"
	if 'username' in session:
		if type == 'customer':
			try:
				newRating = int(request.form['yourRating'])
				return render_template('food.html',
										food = food,
										chef = chef,
										price = price,
										rating = newRating,
										names = names,
										description = description)
			except:
				return render_template('food.html',
										food = food,
										chef = chef,
										price = price,
										rating = rating,
										names = names,
										description = description)
		else:
			return render_template('food.html',
										food = food,
										chef = chef,
										price = price,
										rating = rating,
										names = names,
										description = description)
	else:
		return redirect(url_for('home'))

@app.route("/forum")
def forum():
	users = ["Bob", "Jack", "Jill", "John", "Jane", "Jose", "Jake"]
	# staff = ["Bob", "Jack", "Jill"]
	customers = ["John", "Jane", "Jose"]
	names = ["Jane", "Jose", "Bob"]
	comments = ["Lorem ipsum dolor sit, amet consectetur adipisicing elit.  Accusamus numquam assumenda hic aliquam vero sequi velit molestias doloremque molestiae dicta?", "Lorem ipsum dolor sit, amet consectetur adipisicing elit.  Accusamus numquam assumenda hic aliquam vero sequi velit molestias doloremque molestiae dicta?", "Lorem ipsum dolor sit, amet consectetur adipisicing elit.  Accusamus numquam assumenda hic aliquam vero sequi velit molestias doloremque molestiae dicta?"]
	if 'username' in session:
		if type == 'customer':
			try:
				message = request.form['msg']
				recipient = request.form['recipient']
				return render_template('forum.html',
										people = users,
										names = names)
			except:
				return render_template('forum.html',
										people = users,
										names = names)
		elif type == 'delivery' or type == 'chef':
			try:
				message = request.form['msg']
				recipient = request.form['recipient']
				return render_template('forum.html',
										people = customers,
										names = names)
			except:
				return render_template('forum.html',
										people = customers,
										names = names)
	else:
		return redirect(url_for('home'))

@app.route("/menu")
def menu():
	foodmenu = ['Pizza', 'Sushi']
	return render_template('menu.html', menu = foodmenu)

@app.route("/checkout")
def checkout():
	items = ['Pizza', 'Sushi']
	return render_template('checkout.html', items = items)

@app.route("/logout")
def logout():
	# removes stored data
	session.pop("username")
	
	return redirect(url_for("home"))

if __name__ == "__main__":
	app.secret_key = os.urandom(32)
	app.debug = True
	app.run()