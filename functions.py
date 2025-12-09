from flask import session
from werkzeug.security import generate_password_hash
import mariadb, dotenv, os, secrets, time, random, string

dotenv.load_dotenv()

envhost = os.getenv("DB_HOST")
envuser = os.getenv("DB_USER")
envpassword = os.getenv("DB_PASSWORD")
envdb = os.getenv("DB_NAME")
envtables = os.getenv("DB_TABLES").split(",")
envtablecontent = os.getenv("DB_TABLECONTENT").split("|")

def dbcheck(mycursor, db):
    mycursor.execute("SHOW DATABASES;")
    temp = [x[0] for x in mycursor]
    if db not in temp:
      mycursor.execute(f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
      temp.append(db)

def tablecheck(mycursor, envtables, envtablecontent):
    mycursor.execute("SHOW TABLES;")
    temp = [x[0] for x in mycursor]
    for i, tablename in enumerate(envtables):
      con = envtablecontent[i]
      if tablename not in temp:
          mycursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} {con}")

def tester(mycursor, conn, xtable, val):
    mycursor.execute(f"SELECT COUNT(*) FROM {xtable}")
    count = mycursor.fetchone()[0]
    if count == 0:
        mycursor.execute(f"SELECT * FROM {xtable} LIMIT 0")
        dc = [cl[0] for cl in mycursor.description]
        if "id" in dc:
          dc.remove("id")
        elif "time" in dc:
          dc.remove("time")
        colnames = ", ".join(f"`{c}`" for c in dc)
        placeholders = ", ".join(["%s"] * len(dc))
        mycursor.executemany(f"INSERT INTO {xtable} ({colnames}) VALUES ({placeholders})", val)
        conn.commit()

def testinsert(mycursor, conn, envtables, mariadb):
  userval = [
              ("admin@live.no", generate_password_hash("hemmelig123"), 1, "admin"),
              ("stian@live.no", generate_password_hash("stianpassword"), 1,"kunde"),
              ("petter@live.no", generate_password_hash("petterpassword"), 1,"kunde")
            ]
  productval = [
              ("Tine",  "gulost", 99.9, "FOOD", "Beste osten i byen", "1"),
              ("Tine", "lett melk", 59.9, "FOOD", "Beste melken i byen", "1")
            ]
  try:
      utable = None
      ptable = None
      for t in envtables:
          if "users" in t.lower():
              utable = t
          elif "products" in t.lower():
              ptable = t
      if not utable or not ptable:
          return
      tester(mycursor, conn, utable, userval)
      tester(mycursor, conn, ptable, productval)
  except mariadb.Error as e:
      print(f"Error connecting to MariaDB: {e}")

def get_db_connection():
    return mariadb.connect(
        host = envhost,
        user = envuser,
        password = envpassword,
        database = envdb
    )

def productlistings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    conn.close()
    return result

def init_cart():
    if "cart" not in session or not isinstance(session["cart"], dict):
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

def generate_order_number():
    timestamp = int(time.time())
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    rand = secrets.token_hex(8).upper()
    order_id = f"{timestamp}-{suffix}-{rand}"
    return order_id