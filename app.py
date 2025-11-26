from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import dotenv
import os
import mariadb
import functions

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

limiter = Limiter(get_remote_address, app=app, default_limits=["20 per 10 minutes"])


dotenv.load_dotenv()

#Default Values
envhost = os.getenv("DB_HOST")
envuser = os.getenv("DB_USER")
envpassword = os.getenv("DB_PASSWORD")
envdb = os.getenv("DB_NAME")
envtables = os.getenv("DB_TABLES").split(",")
envtablecontent = os.getenv("DB_TABLECONTENT").split("|")

try:
    mydb = mariadb.connect(
    host = envhost,
    user = envuser,
    password = envpassword,
    )
    mycursor = mydb.cursor()
    functions.dbcheck(mycursor, envdb)
    mydb = mariadb.connect(
    host = envhost,
    user = envuser,
    password = envpassword,
    database = envdb,
    )
    mycursor = mydb.cursor()
    functions.tablecheck(mycursor, envtables, envtablecontent)
    functions.testinsert(mycursor, mydb, envtables, mariadb)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")

def get_db_connection():
    return mariadb.connect(
        host = envhost,
        user = envuser,
        password = envpassword,
        database = envdb
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/registrer", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO users (email, password, active, role) VALUES (%s, %s, %s, %s)", 
                       (email, password, True, 'kunde'))
        mydb.commit()
        cursor.close()
        mydb.close()
        flash("User Registered", "success")
        return redirect(url_for("index"))
    return render_template("registrer.html")

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per 10 minutes")
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email, ))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['email'] = user['email']
            session['role'] = user['role']
            return redirect(url_for("index"))
            # if user['role'] == 'admin':
            #     return redirect(url_for("index"))
            # else:
            #     return redirect(url_for("index"))
        else:
            return render_template("login.html", feil_melding="Incorrect email or password")
    return render_template("login.html")

# @app.route("/admin")
# def admin_dashboard():
#     if session.get("role") == "admin":
#         return render_template("index.html", brukernavn=session['brukernavn'])
#     return redirect(url_for("login"))

# @app.route("/user")
# def user_dashboard():
#     if session.get("role") == "bruker":
#         return render_template("index.html", brukernavn=session['brukernavn'])
#     return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You logget out.", "info")
    return redirect(url_for("login"))

@app.route('/profilepage')
def profilepage():
    return render_template('profilepage.html')

@app.route('/useradministration')
def administrateusers():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    mydb.close()
    return render_template('useradministration.html', users=result)

@app.route('/useradministration/update', methods=['POST'])
def update():
    cid = request.form['id']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    role = request.form['role']
    sql = "UPDATE users SET name=%s, email=%s, password=%s, address=%s, role=%s WHERE id=%s"
    val = (name, email, password, address, role, cid)
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return redirect('/useradministration')

@app.route('/useradministration/delete', methods=['POST'])
def delete():
    cid = request.form['id']
    sql = "DELETE FROM customers WHERE id=%s"
    val = (cid)
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return redirect('/useradministration')

@app.route('/products')
def products():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT companyname, productname, cost, category, description, image FROM products")
    result = cursor.fetchall()
    mydb.close()
    return render_template('products.html', products=result)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)