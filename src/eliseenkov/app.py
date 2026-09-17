from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)  
def connection():
    return mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123")

@app.route('/user_register', methods=['POST'])
def user_register():
    req = request.get_json()
    cnx = connection()
    
    name = req['name']
    login = req['email']
    password = req['password']
    date = (name, login, password)
    cur = cnx.cursor()
    rows = cur.execute('INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', date)
    cnx.commit()
    cnx.close()

    return {}

@app.route('/user_login', methods=['POST'])
def user_login():
    req = request.get_json()
    cnx = connection()
    
    login = req['email']
    password = req['password']
    date = (login, password)
    cur = cnx.cursor()
    rows = cur.execute('SELECT * FROM users WHERE email=%s AND password_hash=%s', date)
    cnx.commit()
    cnx.close()

    return {}
# # Fetch one result
# row = cur.fetchone()
# print("Current date is: {0}".format(row[0]))

# # Close connection
# cnx.close()

@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/login")
def login():
    return render_template('login.html')
app.run()