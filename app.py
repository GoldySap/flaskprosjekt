from flask import Flask, render_template, request, redirect
import dotenv
import os
import mariadb
import functions

app = Flask(__name__)

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
    # functions.tablecheck(mycursor, envtables, envtablecontent)
    # functions.testinsert(mycursor, mydb, envtables, mariadb)
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
    if request.method == 'POST':
        inp = request.form['redirect']
        if inp == "p":
            return redirect('/products')
        elif inp == "t":
            return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    mydb.close()
    return render_template('test.html', users=result)

@app.route('/users/update', methods=['POST'])
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
    return redirect('/users')

@app.route('/users/delete', methods=['POST'])
def delete():
    cid = request.form['id']
    sql = "DELETE FROM customers WHERE id=%s"
    val = (cid)
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return redirect('/users')

@app.route('/products')
def products():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT companyname, productname, cost, category, description, image FROM products")
    result = cursor.fetchall()
    mydb.close()
    return render_template('products.html', products=result)

if __name__ == '__main__':
    app.run(debug=True)