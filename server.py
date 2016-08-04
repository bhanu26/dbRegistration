from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'regform')

app.secret_key = "ThisIsSecret!"

@app.route('/')
def index():
	query = "SELECT * FROM users"
	users = mysql.query_db(query)
	return render_template('index.html', users = users)

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	user = "SELECT * FROM users WHERE users.email = :email LIMIT 1"
	data = {'email': email}
	user = mysql.query_db(user, data)
	print user[0]
	if user[0]:
		if user[0]['password'] == password:
			return render_template('success.html')
		else:
			flash("Wrong credentials")
			return redirect('/')

@app.route('/register', methods=['POST'])
def submit():
	session['first'] = request.form['first']
	session['last'] = request.form['last']
	session['email'] = request.form['email']
	session['password'] = request.form['password']
	error = 0
	if session['first'].isalpha() == False:
		flash("First name cannot contain numbers!")
		error += 1
	if len(request.form['last']) < 1:
		flash("Last name cannot be blank!")
		error += 1
	if len(request.form['first']) < 1:
		flash("First name cannot be blank!")
		error += 1
	if request.form['last'].isalpha() == False:
		flash("Last name cannot contain numbers!")
		error += 1
	if len(request.form['email']) < 1:
		flash("Email cannot be blank!")
		error += 1
	if len(request.form['password']) < 8:
		flash("Password cannot be less than 8 characters!")
		error += 1
	if len(request.form['password']) != len(request.form['confirm']):
		flash("Confirmed password doesn't match!")
		error += 1
	if error > 0:
		return redirect('/')
	if error == 0:
		query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
		data = {
			'first_name': request.form['first'],
			'last_name': request.form['last'],
			'email': request.form['email'],
			'password': request.form['password']
			}
		mysql.query_db(query, data)
		return render_template('success.html')
# @app.route('/add', methods=['POST'])
# def create():
# 	query = "INSERT INTO friends(first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
# 	data = {
# 			'first_name': request.form['first'],
# 			'last_name': request.form['last'],
# 			'email': request.form['email'],
# 			'password': request.form['password']
# 		}
# 	mysql.query_db(query, data)
# 	return redirect('/')

# @app.route('/edit/<friend_id>', methods=['POST'])
# def show(friend_id): #friend_id is the variable that you're passing
# 	query = "SELECT * FROM friends WHERE id = :specific_id" #this is the query you're sending to the database
# 	data = {'specific_id': friend_id} # this is the data you're sending to the datbase
# 	friends = mysql.query_db(query, data) #combine the query with the data and you'll get back data from the database
# 	return render_template('edit.html', friends=friends) #this sends you to the edit.html page with friends being the data you requested

@app.route('/delete/<user_id>')
def delete(user_id):
	query = "DELETE FROM users WHERE id = :id" #this is the query
	data = {'id': user_id} #this is the data
	mysql.query_db(query, data) #this is the result from the query with the data from the db
	return redirect('/') #redirect back to the front page

# @app.route('/update/<friend_id>', methods=['POST'])
# def update(friend_id):
# 	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation, updated_at = NOW() WHERE id = :id" #the query that you're updating info from the db back to the db
# 	data = { #this is the data you'll be updating in the db
# 		'first_name': request.form['first_name'], 
# 		'last_name':  request.form['last_name'],
# 		'occupation': request.form['occupation'],
# 		'id': friend_id
# 		}
# 	mysql.query_db(query, data)
# 	return redirect('/')

app.run(debug=True)