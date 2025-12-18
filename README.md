# Flask-prosjekt -- Dokumentasjon
## 1. Forside
### Prosjekttittel: Nettbutikk
Navn: Alexander \
Klasse: 2IMI \
Dato: 11.11.2025

### Kort beskrivelse av prosjektet:
Prosjektet går ut på at jeg skal lage en nettbutikk, der jeg utnytter 3 eller flere tabeler fra en database.
Prosjektet går ut på å utvikle en nettbutikk ved hjelp av Flask og MariaDB. Applikasjonen benytter flere tabeller i databasen for å håndtere brukere, produkter, kjøp og betalingsinformasjon.

---

## 2. Systembeskrivelse
### Formål med applikasjonen:
Formålet med applikasjonen er å tilby en fungerende nettbutikk med følgende funksjonalitet:

* Produktkatalog
* Innlogging og registrering av brukere
* Handlekurv for valgte produkter
* Kvittering og kjøpshistorikk
* Brukerinnstillinger og profilsider

### Brukerflyt:
Brukeren starter på hjemmesiden. Via navigasjonsmenyen kan brukeren:

* Logge inn eller registrere seg
* Se og redigere profilsiden sin
* Bla gjennom produktkatalogen
* Legge produkter i handlekurven
* Fullføre kjøp og se ordrebekreftelse
* Returnere til hjemmesiden når som helst

### Teknologier brukt:
* **Backend:** Python / Flask
* **Database:** MariaDB
* **Frontend:** HTML, CSS, JavaScript, jQuery

---

## 3. Server-, infrastruktur- og nettverksoppsett
### Servermiljø
* **Server:** Raspberry Pi
* **Operativsystem:** Ubuntu Server

### Nettverksoppsett:

Nettverksdiagram:\
<img width="424" height="384" alt="Diagram" src="https://github.com/user-attachments/assets/8722f083-4119-4ba0-b96c-180cca1bea69" />

* **IP-adresse:** 10.200.14.20
* **Porter:** 80 (HTTP)
* **Brannmur:** Kun nødvendige porter åpne

Eksempel:
Klient → MariaDB
Tjenestekonfigurasjon
systemctl / Supervisor\
Filrettigheter\
Miljøvariabler

---

## 4. Prosjektstyring -- GitHub Projects (Kanban)

Prosjektet benyttet GitHub Projects med Kanban-tavle:

* **Backlog**
* **Ready**
* **In Progress**
* **In Review**
* **Done**

### Refleksjon
Kanban-metoden gjorde det enklere å planlegge arbeidet, holde oversikt over fremdrift og prioritere oppgaver underveis i prosjektet.

---

## 5. Databasebeskrivelse

**Databasenavn:** nettbutikk

**Diagram:** \
<img width="439" height="301" alt="Nettbutikk_Diagram" src="https://github.com/user-attachments/assets/a543641c-a9c9-46d3-aef0-c72f7029c825" />

### Tabeller

#### users

| Tabell | Felt     | Datatype     | Beskrivelse          |
| -------| -------- | ------------ | -------------------- |
| users  | id       | INT          | Primærnøkkel         |
| users  | email    | VARCHAR(255) | Brukerens e-post     |
| users  | password | VARCHAR(255) | Hashet passord       |
| users  | active   | BOOL         | Aktiv/inaktiv bruker |
| users  | role     | VARCHAR(255) | Brukerrolle          |

#### products

| Tabell   | Felt        | Datatype     | Beskrivelse  |
| -------- | ----------- | ------------ | ------------ |
| products | id          | INT          | Primærnøkkel |
| products | companyname | VARCHAR(255) | Leverandør   |
| products | productname | VARCHAR(255) | Produktnavn  |
| products | cost        | FLOAT        | Pris         |
| products | category    | VARCHAR(255) | Kategori     |
| products | description | VARCHAR(255) | Beskrivelse  |
| products | image       | VARCHAR(255) | Bilde-URL    |

#### credentials

| Tabell      | Felt           | Datatype     | Beskrivelse           |
| ----------- | -------------- | ------------ | --------------------- |
| credentials | id             | INT          | Primærnøkkel          |
| credentials | cardnumber     | VARCHAR(255) | Kortnummer            |
| credentials | expirationdate | VARCHAR(255) | Utløpsdato            |
| credentials | securitycode   | INT          | Sikkerhetskode        |
| credentials | userid         | INT          | Referanse til bruker  |
| credentials | active         | BOOL         | Aktiv betalingsmetode |

#### billing

| Tabell  | Felt        | Datatype     | Beskrivelse          |
| ------- | ----------- | ------------ | -------------------- |
| billing | id          | INT          | Primærnøkkel         |
| billing | firstname   | VARCHAR(255) | Fornavn              |
| billing | lastname    | VARCHAR(255) | Etternavn            |
| billing | adressline1 | VARCHAR(255) | Adresse              |
| billing | adressline2 | VARCHAR(255) | Tilleggsadresse      |
| billing | country     | VARCHAR(255) | Land                 |
| billing | state       | VARCHAR(255) | Fylke                |
| billing | city        | VARCHAR(255) | By                   |
| billing | zip         | INT          | Postnummer           |
| billing | phonenumber | INT          | Telefonnummer        |
| billing | userid      | INT          | Referanse til bruker |
| billing | active      | BOOL         | Aktiv adresse        |

#### recipt (kvittering)

| Tabell | Felt         | Datatype     | Beskrivelse     |
| ------ | ------------ | ------------ | --------------- |
| recipt | id           | INT          | Primærnøkkel    |
| recipt | ordernumber  | VARCHAR(100) | Ordrenummer     |
| recipt | time         | TIMESTAMP    | Kjøpstidspunkt  |
| recipt | cost         | FLOAT        | Totalpris       |
| recipt | userid       | INT          | Bruker          |
| recipt | productid    | INT          | Produkt         |
| recipt | credentialid | INT          | Betalingsmetode |
| recipt | billingid    | INT          | Fakturaadresse  |

---

SQL-eksempel:

CREATE TABLE users ( \
  id INT AUTO_INCREMENT PRIMARY KEY, \
  email VARCHAR(255), \
  password VARCHAR(255), \
  active BOOL, \
  role VARCHAR(255) \
);

CREATE TABLE products ( \
  id INT AUTO_INCREMENT PRIMARY KEY, \
  companyname VARCHAR(255) NOT NULL, \
  productname VARCHAR(255) NOT NULL, \
  cost FLOAT NOT NULL, \
  category VARCHAR(255), \
  description VARCHAR(255), \
  image VARCHAR(255) \
);

CREATE TABLE credentials ( \
  id INT AUTO_INCREMENT PRIMARY KEY, \
  cardnumber VARCHAR(255) NOT NULL, \
  expirationdate VARCHAR(255) NOT NULL, \
  securitycode VARCHAR(255) NOT NULL, \
  userid INT, \
  active BOOL, \
  FOREIGN KEY (userid) REFERENCES users(id) \
);

CREATE TABLE billing ( \
  id INT AUTO_INCREMENT PRIMARY KEY, \
  firstname VARCHAR(255), \
  lastname VARCHAR(255) NOT NULL, \
  adressline1 VARCHAR(255), \
  adressline2 VARCHAR(255), \
  country VARCHAR(255), \
  state VARCHAR(255), \
  city VARCHAR(255), \
  zip INT, phonenumber INT, \
  userid INT, active BOOL, \
  FOREIGN KEY (userid) REFERENCES users(id) \
);

CREATE TABLE recipt ( \
  id INT AUTO_INCREMENT PRIMARY KEY, \
  ordernumber VARCHAR(100) NOT NULL UNIQUE, \
  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, \
  cost FLOAT, \
  userid INT, \
  productid INT, \
  credentialid INT, \
  billingid INT, \
  FOREIGN KEY (userid) REFERENCES users(id), \
  FOREIGN KEY (productid) REFERENCES products(id), \
  FOREIGN KEY (credentialid) REFERENCES credentials(id), \
  FOREIGN KEY (billingid) REFERENCES billing(id)) \
);

---

## 6. Programstruktur
projectnavn \
  ├ static \
  │    ├──css \
  │    │  ├──style.js \
  │    │  ├──profile.js \
  │    │  ├──loginregister.js \
  │    │  ├──products.js \
  │    │  ├──menu.js \
  │    │  └──administration.html \
  │    ├──images \
  │    └──js \
  │       ├──layout.js \
  │       ├──profile.js \
  │       ├──administration.js \
  │       └──loginregister.js \
  ├── templates \
  │    ├──index.html \
  │    ├──layout.html \
  │    ├──profile.html \
  │    ├──products.html \
  │    ├──checkout.html \
  │    ├──ordersuccess.html \
  │    ├──login.html \
  │    ├──profile.html \
  │    ├──products.html \
  │    └──administration.html \
  ├── .env \
  ├── .gitingnore \
  ├── app.py \
  ├── functions.py \
  ├── inspiration.py \
  └── README.md \
Databasestrøm:
HTML → Flask → MariaDB → Flask → HTML-tabell\
eller\
HTML → JS/Jquery → Flask → MariaDB → Flask → HTML\

---

## 7. Kodeforklaring
Her forklares hovedrutene i Flask-applikasjonen, for eksempel:

* `try/except` - håndterer auto oppretelsen av databasen og legger til test kontoer og produkter, hvis de ikke allerede eksisterer.
```python
# Skjekker om databasen eksisterer, og oppretter den hvis ikke
def dbcheck(mycursor, db):
    mycursor.execute("SHOW DATABASES;")
    temp = [x[0] for x in mycursor]
    if db not in temp:
      mycursor.execute(f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
      temp.append(db)

# Skjekker om de nødvendige tabelene i databasen eksisterer, og oppretter dem hvis ikke
def tablecheck(mycursor, envtables, envtablecontent):
    mycursor.execute("SHOW TABLES;")
    temp = [x[0] for x in mycursor]
    for i, tablename in enumerate(envtables):
      con = envtablecontent[i]
      if tablename not in temp:
          mycursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} {con}")

# Sender en gitt verdi til den spesifiserte tabelen
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

# Setter in test kontoene og produktene i de relevante tabelene, hvis de ikke eksisterer
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

# Skaper tilkobling til databasen
def get_db_connection():
    return mariadb.connect(
        host = envhost,
        user = envuser,
        password = envpassword,
        database = envdb
    )

# Kobler til serveren og skjekker om databasen og alle nødvendige tabeller eksisterer, så legger til test verdier om de ikke eksisterer
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
```

* `/login` – håndterer innlogging
```python
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per 1 minutes")
def login():
    if request.method == "POST":
        # Henter innloggings info fra innloggings formen
        email = request.form['email']
        password = request.form['password']

        # Skaper tilkopling til databasen og henter den samsvarende kontoen til emailen angitt, hvis the er aktiv
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND active=1", (email, ))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Skjekker om brukeren finnes, og om passordet matcher den samsvarende kontoen og om kontoen er aktive
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
```

* `/register` – registrering av brukere
```python
@app.route("/registrer", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Henter innloggings info fra innloggings formen
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
```

* `/products` – viser produktkatalog
```python
# Henter produktene fra product tabellen
def productlistings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    conn.close()
    return result

# Opner siden med angitt produkter til å hvise dem grafiskk
@app.route("/products")
def products():
    result = productlistings()
    return render_template("products.html", products=result)
```

* `/checkout` – gjennomfører kjøp
```python
@app.route("/checkout")
def checkout():
    if "id" not in session:
        return redirect("/login")

    user_id = session.get("id")

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
```
---

## 8. Sikkerhet og pålitelighet

* Environment file (`.env`) brukt til oppbevaring av sensitive verdier.
* Miljøvariabler for databasepålogging,  databasestruktur og sikkerhets nøkkel
* Parameteriserte SQL-spørringer
* Validering av input fra bruker
* Feilhåndtering med `try/except`, `verdi sammenligning` og regulerte handlinger om hvise krav ikke møtes.

---

## 9. Feilsøking og testing
### Typiske feil

* Databaseforbindelse feilet
* Feil i SQL-spørringer
* Manglende validering av input
* Syntaxs

### Løsning

Feil ble løst ved:
* Bruk av logging
* Utskrift i konsoll
* Testing av SQL-spørringer direkte i databasen.
* Ssh tilkobling til serveren for administrering av databasen direkte og værifisering av resultater.

### Testmetoder

* Manuell testing av alle sider
* Testing med ulike brukere og roller
* Konsoll Utskrivelser

---

## 10. Konklusjon og refleksjon

### Hva lærte du?

Jeg lærte hvordan man bygger en fullstack-applikasjon med HTML, CSS, JS, PYTHON Flask og Mariadb database.

### Hva fungerte bra?

Databasekobling og struktur fungerte stabilt.

### Hva var utfordrende?

Håndtering av relasjoner mellom tabeller og feilsøking i backend.

### Hva ville du gjort annerledes?

Jeg ville planlagt databasemodellen enda bedre før koding startet.
