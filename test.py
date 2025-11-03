from flask import Flask, render_template, request, redirect
import mariadb

app = Flask(__name__)

def get_db_connection():
    return mariadb.connect(
        host="10.200.14.20",
        user="lit",
        password="ons",
        database="flask_db"
    )

@app.route('/')
def index():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    mydb.close()
    return render_template('test.html', users=result)

@app.route('/update', methods=['POST'])
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

@app.route('/delete', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
