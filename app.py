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
envdatabase = os.getenv("DB_NAME")
envtables = os.getenv("DB_TABLES").split(",")
envtablecontent = os.getenv("DB_TABLECONTENT").split(",")

envdb = envdatabase

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

@app.route('/')
def index():
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
    address = request.form['address']
    sql = "UPDATE users SET name=%s, address=%s WHERE id=%s"
    val = (name, address, cid)
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return redirect('/')

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
    return redirect('/')

@app.route('/products')
def products():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT name, pris FROM products")
    result = cursor.fetchall()
    mydb.close()
    return render_template('products.html', products=result)

if __name__ == '__main__':
    app.run(debug=True)