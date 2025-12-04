from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from pythonmonkey import require as js_require
import dotenv
import os
import mariadb
import functions

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per 5 minutes"])

dotenv.load_dotenv()

#Default Values
envhost = os.getenv("DB_HOST")
envuser = os.getenv("DB_USER")
envpassword = os.getenv("DB_PASSWORD")
envdb = os.getenv("DB_NAME")
envtables = os.getenv("DB_TABLES").split(",")
envtablecontent = os.getenv("DB_TABLECONTENT").split("|")

# js_lib = js_require('./administration.js')

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
        password_raw = request.form['password']
        repassword_raw = request.form['retypeinput']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email, ))
        existing = cursor.fetchone()
        cursor.close()
        conn.close()
        if existing:
            return render_template("login.html", feil_melding="Email already in use")

        if password_raw != repassword_raw:
            return render_template("login.html", feil_melding="Password mismatch")
        
        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO users (email, password, active, role) VALUES (%s, %s, %s, %s)", (email, password, True, 'kunde'))
        mydb.commit()
        cursor.close()
        mydb.close()
        flash("User Registered", "success")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email, ))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        session['email'] = user['email']
        session['role'] = user['role']
        return redirect(url_for("index"))
    return render_template("login.html")

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
        if user and check_password_hash(user['password'], password) and user['active']:
            session['email'] = user['email']
            session['role'] = user['role']
            return redirect(url_for("index"))
        else:
            return render_template("login.html", feil_melding="Incorrect email or password")
    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You logget out.", "info")
    return redirect("/")

@app.route('/administration')
def administration(admin):
    if admin == "useradministration":
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        mydb.close()
    if admin == "productadministration":
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        result = cursor.fetchall()
        mydb.close()
    return render_template('administration.html', results=result, x=admin)

@app.route('/administration/update', methods=['POST'])
def update(admin):
    if admin == "useradministration":
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
    if admin == "productadministration":
        cid = request.form['id']
        companyname = request.form['companyname']
        productname = request.form['productname']
        cost = request.form['cost']
        category = request.form['category']
        description = request.form['description']
        image = request.form['image']
        sql = "UPDATE products SET companyname=%s, productname=%s, cost=%s, category=%s, description=%s, image=%s WHERE id=%s"
        val = (companyname, productname, cost, category, description, image, cid)
        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
    return redirect('/administration')

@app.route('/administration/delete', methods=['POST'])
def delete(admin):
    if admin == "useradministration":
        cid = request.form['id']
        sql = "DELETE FROM users WHERE id=%s"
        val = (cid)
        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
    if admin == "productadministration":
        cid = request.form['id']
        sql = "DELETE FROM products WHERE id=%s"
        val = (cid)
        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
    return redirect('/administration')

def productlistings():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    mydb.close()
    return result

def init_cart():
    if "cart" not in session:
        session["cart"] = {}

def add_to_cart(product_id, quantity):
    init_cart()
    cart = session["cart"]

    product_id = str(product_id)
    quantity = int(quantity)

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    session["cart"] = cart


def remove_from_cart(product_id):
    init_cart()
    cart = session["cart"]
    cart.pop(str(product_id), None)
    session["cart"] = cart

@app.route("/products")
def products():
    result = productlistings()
    return render_template("products.html", products=result)


@app.route("/add", methods=["POST"])
def add():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity", 1)
    add_to_cart(product_id, quantity)
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    result = productlistings()
    init_cart()
    cart_items = []
    total = 0

    for pid, qty in session["cart"].items():
        product = None
        for p in result:
            if str(p["id"]) == pid:
                product = p
                break
        print("PRODUCTS:", result)
        if product:
            subtotal = product["cost"] * qty
            total += subtotal
            cart_items.append({
                "name": product["productname"],
                "price": product["cost"],
                "qty": qty,
                "subtotal": subtotal,
                "id": pid,
                "image": product["image"]
            })

    return render_template("cart.html", cart=cart_items, total=total)


@app.route("/cart/remove/<id>")
def remove(id):
    remove_from_cart(id)
    return redirect(url_for("cart"))

@app.route('/profile')
def profile():
    return render_template('profilepage.html')

@app.route('/settings')
def settings():
    return render_template('profilepage.html')


@app.route('/routing', methods=['GET', 'POST'])
def routing():
    data = request.get_json(force=True)
    
    if not data or "param" not in data:
        return {"message": "Invalid request"}, 400
    
    route = data["param"]
  
    match route:
        case "profile" | "settings" | "logout":
            return {"redirect": url_for(route)}
        case "useradministration" | "productadministration":
            if session.get("role") == "admin":
                return {"redirect": url_for("administration", admin=route)}
            return {"message": "You do not have permission"}, 403
    return {"message": "Unknown route"}, 400


if __name__ == '__main__':
    app.run(debug=True)