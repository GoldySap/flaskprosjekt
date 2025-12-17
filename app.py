from functions import *
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from flask_wtf.csrf import CSRFProtect, generate_csrf
# from pythonmonkey import require as js_require
import hashlib, dotenv, os, mariadb

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

limiter = Limiter(get_remote_address, app=app, default_limits=["100 per 1 minutes"])

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
    conn = mariadb.connect(
    host = envhost,
    user = envuser,
    password = envpassword,
    )
    mycursor = conn.cursor()
    dbcheck(mycursor, envdb)
    conn = mariadb.connect(
    host = envhost,
    user = envuser,
    password = envpassword,
    database = envdb,
    )
    mycursor = conn.cursor()
    tablecheck(mycursor, envtables, envtablecontent)
    testinsert(mycursor, conn, envtables, mariadb)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/registrer", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password_raw = request.form['password']
        repassword_raw = request.form['retypeinput']
        password = request.form['password']

        hashed = hashlib.sha256(password.encode()).hexdigest()

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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password, active, role) VALUES (%s, %s, %s, %s)", (email, hashed, True, 'kunde'))
        conn.commit()
        cursor.close()
        conn.close()
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
        cursor.execute("SELECT * FROM users WHERE email=%s AND active=1", (email, ))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user == None:
            return render_template("login.html", feil_melding="Account not found")
        if user and check_password_hash(user['password'], password) and user['active']:
            session['id'] = user['id']
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
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        conn.close()
    if admin == "productadministration":
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        result = cursor.fetchall()
        conn.close()
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
    return redirect('/administration')

@app.route('/administration/delete', methods=['POST'])
def delete(admin):
    if admin == "useradministration":
        cid = request.form['id']
        sql = "DELETE FROM users WHERE id=%s"
        val = (cid)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
    if admin == "productadministration":
        cid = request.form['id']
        sql = "DELETE FROM products WHERE id=%s"
        val = (cid)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
    return redirect('/administration')

@app.route("/products")
def products():
    result = productlistings()
    return render_template("products.html", products=result)


@app.post("/add")
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
        if product:
            subtotal = round(product["cost"] * qty, 2)
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

@app.route("/checkout")
def checkout():
    if "id" not in session:
        return redirect("/login")

    user_id = session["id"]

    products = productlistings()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM billing WHERE userid=%s AND active=1", (user_id,))
    billing = cursor.fetchone()

    cursor.execute("SELECT * FROM credentials WHERE userid=%s AND active=1", (user_id,))
    card = cursor.fetchone()

    cursor.close()
    conn.close()

    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for pid, qty in cart.items():
        product = next((p for p in products if str(p["id"]) == str(pid)), None)
        if product:
            subtotal = round(product["cost"] * qty, 2)
            total += subtotal
            cart_items.append({
                "id": product["id"],
                "name": product["productname"],
                "price": product["cost"],
                "qty": qty,
                "subtotal": subtotal,
                "image": product["image"]
            })

    return render_template(
        "checkout.html",
        cart=cart_items,
        billing=billing,
        card=card,
        total=total
    )


@app.post("/checkout/complete")
def checkout_complete():
    user_id = session.get("id")
    cart = session.get("cart", {})
    products = productlistings()

    if not cart:
        return redirect("/cart")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM billing WHERE userid=%s AND active=1", (user_id,))
    billing = cursor.fetchone()

    cursor.execute("SELECT id FROM credentials WHERE userid=%s AND active=1", (user_id,))
    card = cursor.fetchone()

    if not billing or not card:
        return redirect("/checkout")
    
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for pid, qty in cart.items():
        product = next((p for p in products if str(p["id"]) == str(pid)), None)
        if product:
            subtotal = round(product["cost"] * qty, 2)
            total += subtotal
            cart_items.append({
                "id": product["id"],
                "name": product["productname"],
                "price": product["cost"],
                "qty": qty,
                "subtotal": subtotal,
                "image": product["image"]
            })

    while True:
        for item in cart_items:
            order_id = generate_order_number()
            cursor.execute("SELECT 1 FROM recipt WHERE ordernumber=%s", (order_id,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO recipt (ordernumber, cost, userid, productid, credentialid, billingid)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (order_id, item["subtotal"], user_id, item["id"], card["id"], billing["id"]))
                conn.commit()
        break

    cursor.close()
    conn.close()

    session["cart"] = []

    return render_template("ordersuccess.html", order_id=order_id)


@app.route("/order-success/<int:order_id>")
def order_success(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM recipt WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    cursor.execute("""
        SELECT oi.*, p.productname FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        WHERE oi.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("ordersuccess.html", order=order, items=items)

@app.get("/profile")
def profile():
    user_id = session["id"]
    if not user_id:
        return redirect("/login")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT email FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT cardnumber, expirationdate, securitycode FROM credentials WHERE userid=%s AND active=1", (user_id,))
    bank = cursor.fetchone()

    cursor.execute("SELECT firstname, lastname, adressline1, adressline2, country, state, city, zip, phonenumber FROM billing WHERE userid=%s AND active=1", (user_id,))
    billing = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("profile.html", user=user, bank=bank, billing=billing)

@app.post("/profile/bank")
def profile_bank():
    user_id = session.get("id")
    card = generate_password_hash(request.form.get("card"))
    exp = generate_password_hash(request.form.get("exp"))
    cvv = generate_password_hash(request.form.get("cvv"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO credentials (cardnumber, expirationdate, securitycode, userid, active)
        VALUES (%s, %s, %s, %s, 1)
    """, (card, exp, cvv, user_id))

    conn.commit()
    cursor.close()
    conn.close()
    return "OK"

@app.post("/profile/billing")
def update_billing():
    user_id = session.get("id")

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    line1 = request.form.get("adressline1")
    line2 = request.form.get("adressline2")
    country = request.form.get("country")
    state = request.form.get("state")
    city = request.form.get("city")
    zip_code = request.form.get("zip")
    phone = request.form.get("phonenumber")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE billing SET active=0 WHERE userid=%s", (user_id,))
    cursor.execute("""
        INSERT INTO billing (
            firstname, lastname, adressline1, adressline2,
            country, state, city, zip, phonenumber, userid, active
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
    """, (firstname, lastname, line1, line2, country, state, city, zip_code, phone, user_id))

    conn.commit()
    cursor.close()
    conn.close()
    return "OK"

@app.post("/profile/email")
def update_email():
    user_id = session.get("id")
    new_email = request.form["email"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE users SET email=%s WHERE id=%s", (new_email, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return "OK"

@app.post("/profile/password")
def update_password():
    user_id = session.get("id")
    new = request.form["password"]
    confirm = request.form["confirm"]

    if new != confirm:
        return "Passwords do not match", 400

    hashed = hashlib.sha256(new.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return "OK"

@app.post("/profile/delete")
def delete_account():
    user_id = session.get("id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE users SET active=0 WHERE id=%s", (user_id,))
    cursor.execute("UPDATE credentials SET active=0 WHERE userid=%s", (user_id,))
    cursor.execute("UPDATE billing SET active=0 WHERE userid=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    session.clear()
    return "OK"


@app.route('/settings')
def settings():
    return render_template('profile.html')


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