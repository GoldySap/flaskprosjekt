# Flask-prosjekt -- Dokumentasjon
## 1. Forside
### Prosjekttittel: Nettbutikk
Navn: Alexander \
Klasse: 2IMI \
Dato: 11.11.2025

### Kort beskrivelse av prosjektet:
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
Klient → Flask-server → MariaDB → Flask → Klient\
Tjenestekonfigurasjon\
systemctl\
Filrettigheter\
Miljøvariabler

---

## 4. Prosjektstyring -- GitHub Projects (Kanban)

Prosjektet benyttet GitHub Projects med Kanban-tavle:

### Struktur
* **Backlog**
* **Ready**
* **In Progress**
* **In Review**
* **Done**

### Bilder
<img width="823" height="312" alt="image" src="https://github.com/user-attachments/assets/b4b9f3fa-6bd9-472e-a610-8fadfbfea749" />

<img width="546" height="312" alt="image" src="https://github.com/user-attachments/assets/53debf35-d45a-409d-a58f-2c1527fcddb1" />

### Refleksjon
Kanban gjorde det enklere å planlegge arbeidet, holde oversikt over fremdrift og prioritere oppgaver underveis i prosjektet.

---

## 5. Databasebeskrivelse

**Databasenavn:** nettbutikk

**Diagram:** \
<img width="439" height="301" alt="Nettbutikk_Diagram" src="https://github.com/user-attachments/assets/a543641c-a9c9-46d3-aef0-c72f7029c825" />

---

### Databasestruktur og relasjoner
Databasen er bygget opp for å støtte funksjonaliteten i nettbutikken, med tydelige relasjoner mellom brukere, produkter og kjøp. Strukturen er normalisert for å unngå duplisering av data og for å gjøre systemet mer oversiktlig, sikkert og skalerbart.

#### Overordnet sammenheng
Relasjonene mellom tabellene er implementert ved hjelp av fremmednøkler (FOREIGN KEY), som sikrer dataintegritet og forhindrer at kjøp kan eksistere uten gyldig bruker, produkt, betalingsmetode eller adresse.
- En **bruker** kan ha:
  - flere betalingsmetoder (`credentials`)
  - flere fakturaadresser (`billing`)
  - flere kjøp (`recipt`)
- Hvert kjøp er knyttet til:
  - en bruker
  - ett produkt
  - en betalingsmetode
  - en fakturaadresse

Dette gjør det mulig å lagre full kjøpshistorikk og samtidig holde brukerdata strukturert.

---

### Forklaring av tabellene og hvordan de henger sammen

#### users
`users` er kjernetabellen i databasen. Den inneholder all grunnleggende informasjon om brukere, som e-post, passord, rolle og om kontoen er aktiv.

Primærnøkkelen `id` brukes som fremmednøkkel i flere andre tabeller for å knytte data til riktig bruker.

---

#### products
`products` inneholder alle produkter som vises i nettbutikken. Hvert produkt har informasjon som navn, pris, kategori, beskrivelse og bilde.

Produkter kobles til kjøp gjennom `recipt`-tabellen, som gjør det mulig å se hvilke produkter en bruker har kjøpt.

---

#### credentials
`credentials` lagrer betalingsinformasjon for brukere. Tabellen er koblet til `users` via feltet `userid`, som er en fremmednøkkel til `users(id)`.

Dette gjør det mulig for én bruker å ha flere betalingsmetoder, samtidig som betalingsinformasjonen holdes adskilt fra brukerens hovedprofil.

Feltet `active` brukes til å markere hvilken betalingsmetode som er aktiv ved gjennomføring av kjøp.

---

#### billing
`billing` inneholder faktura- og leveringsadresser. Tabellen er også koblet til `users` via `userid`.

Ved å lagre adresser i en egen tabell kan brukere ha flere adresser, og systemet kan enkelt endre hvilken adresse som er aktiv uten å påvirke tidligere kjøp.

---

#### recipt (kvittering)
`recipt` representerer gjennomførte kjøp og fungerer som en kobling mellom flere deler av systemet.

Hver kvittering er knyttet til:
- `userid` → hvilken bruker som har gjennomført kjøpet
- `productid` → hvilket produkt som er kjøpt
- `credentialid` → hvilken betalingsmetode som ble brukt
- `billingid` → hvilken fakturaadresse som ble brukt

Denne strukturen gjør det mulig å vise kjøpshistorikk, generere kvitteringer og dokumentere tidligere ordre selv om bruker senere endrer adresse eller betalingsinformasjon.

---

### Begrunnelse for valg av databasestruktur

Denne databasemodellen er valgt fordi:
- Den følger prinsipper for relasjonsdatabaser
- Den reduserer dataduplisering
- Den gjør systemet enkelt å utvide med flere produkter, adresser og betalingsmetoder
- Den støtter sikker og strukturert lagring av bruker- og kjøpsdata

---

### Tabeller
#### users tabell

| Tabell | Felt     | Datatype     | Beskrivelse          |
| -------| -------- | ------------ | -------------------- |
| users  | id       | INT          | Primærnøkkel         |
| users  | email    | VARCHAR(255) | Brukerens e-post     |
| users  | password | VARCHAR(255) | Hashet passord       |
| users  | active   | BOOL         | Aktiv/inaktiv bruker |
| users  | role     | VARCHAR(255) | Brukerrolle          |

#### products tabell

| Tabell   | Felt        | Datatype     | Beskrivelse  |
| -------- | ----------- | ------------ | ------------ |
| products | id          | INT          | Primærnøkkel |
| products | companyname | VARCHAR(255) | Leverandør   |
| products | productname | VARCHAR(255) | Produktnavn  |
| products | cost        | FLOAT        | Pris         |
| products | category    | VARCHAR(255) | Kategori     |
| products | description | VARCHAR(255) | Beskrivelse  |
| products | image       | VARCHAR(255) | Bilde-URL    |

#### credentials tabell

| Tabell      | Felt           | Datatype     | Beskrivelse           |
| ----------- | -------------- | ------------ | --------------------- |
| credentials | id             | INT          | Primærnøkkel          |
| credentials | cardnumber     | VARCHAR(255) | Kortnummer            |
| credentials | expirationdate | VARCHAR(255) | Utløpsdato            |
| credentials | securitycode   | INT          | Sikkerhetskode        |
| credentials | userid         | INT          | Referanse til bruker  |
| credentials | active         | BOOL         | Aktiv betalingsmetode |

#### billing tabel

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

#### recipt (kvittering) tabell

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
#### users tabell
```sql
CREATE TABLE users ( 
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255), 
  password VARCHAR(255), 
  active BOOL, 
  role VARCHAR(255) 
);
```

#### products tabell
```sql
CREATE TABLE products ( 
  id INT AUTO_INCREMENT PRIMARY KEY, 
  companyname VARCHAR(255) NOT NULL,
  productname VARCHAR(255) NOT NULL, 
  cost FLOAT NOT NULL, 
  category VARCHAR(255), 
  description VARCHAR(255), 
  image VARCHAR(255) 
);
```

#### credentials tabell
```sql
CREATE TABLE credentials ( 
  id INT AUTO_INCREMENT PRIMARY KEY, 
  cardnumber VARCHAR(255) NOT NULL, 
  expirationdate VARCHAR(255) NOT NULL, 
  securitycode VARCHAR(255) NOT NULL, 
  userid INT, 
  active BOOL, 
  FOREIGN KEY (userid) REFERENCES users(id) 
);
```

#### billing tabell
```sql
CREATE TABLE billing ( 
  id INT AUTO_INCREMENT PRIMARY KEY, 
  firstname VARCHAR(255), 
  lastname VARCHAR(255) NOT NULL, 
  adressline1 VARCHAR(255), 
  adressline2 VARCHAR(255), 
  country VARCHAR(255), 
  state VARCHAR(255), 
  city VARCHAR(255), 
  zip INT, phonenumber INT, 
  userid INT, active BOOL, 
  FOREIGN KEY (userid) REFERENCES users(id) 
);
```

#### recipt (kvittering) tabell
```sql
CREATE TABLE recipt ( 
  id INT AUTO_INCREMENT PRIMARY KEY, 
  ordernumber VARCHAR(100) NOT NULL UNIQUE, 
  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, 
  cost FLOAT, 
  userid INT, 
  productid INT, 
  credentialid INT, 
  billingid INT, 
  FOREIGN KEY (userid) REFERENCES users(id), 
  FOREIGN KEY (productid) REFERENCES products(id), 
  FOREIGN KEY (credentialid) REFERENCES credentials(id), 
  FOREIGN KEY (billingid) REFERENCES billing(id)) 
);
```

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
HTML → Flask → MariaDB → Flask → HTML\
eller\
HTML → JS/Jquery → Flask → MariaDB → Flask → HTML\

---

## 7. Kodeforklaring
Her forklares hovedrutene i Flask-applikasjonen, for eksempel:

* `try/except` - håndterer auto oppretelsen av databasen og legger til test kontoer og produkter, hvis de ikke allerede eksisterer.
```python
# Sjekker om databasen eksisterer, og oppretter den hvis ikke
def dbcheck(mycursor, db):
    mycursor.execute("SHOW DATABASES;")
    temp = [x[0] for x in mycursor]
    if db not in temp:
      mycursor.execute(f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
      temp.append(db)

# Sjekker om de nødvendige tabellene i databasen eksisterer, og oppretter dem hvis ikke
def tablecheck(mycursor, envtables, envtablecontent):
    mycursor.execute("SHOW TABLES;")
    temp = [x[0] for x in mycursor]
    for i, tablename in enumerate(envtables):
      con = envtablecontent[i]
      if tablename not in temp:
          mycursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} {con}")

# Sender en gitt verdi til den spesifiserte tabellen
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

# Setter in test kontoene og produktene i de relevante tabellene, hvis de ikke eksisterer
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

# Kobler til serveren og sjekker om databasen og alle nødvendige tabeller eksisterer, så legger til test verdier om de ikke eksisterer
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

        # Sjekker om brukeren finnes, og om passordet matcher den samsvarende kontoen og om kontoen er aktive
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

        # Prøver å hente en konto med samme email
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email, ))
        existing = cursor.fetchone()
        cursor.close()
        conn.close()

        # Sjekker om kontoen allerede finnes
        if existing:
            return render_template("login.html", feil_melding="Email already in use")
        # Sjekker om brukeren skrev passordet feil på passord og repassord(passordet skrevet for en andre gang som at man ikke lagrer feil passord)
        if password_raw != repassword_raw:
            return render_template("login.html", feil_melding="Password mismatch")
        
        # Legger til kontoen i bruker tabellen
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password, active, role) VALUES (%s, %s, %s, %s)", (email, hashed, True, 'kunde'))
        conn.commit()
        cursor.close()
        conn.close()
        flash("User Registered", "success")

        # Setter relevant session info, gjør det samme som login 
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email, ))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        session['id'] = user['id']
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
# Viser aktiv billing og bank info, og valgte produkter og deres total pris
@app.route("/checkout")
def checkout():
    # Sjekker om du ikke er logget inn
    if "id" not in session:
        return redirect("/login")

    user_id = session.get("id")

    products = productlistings()
    
    # Henter billing og bank info
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM billing WHERE userid=%s AND active=1", (user_id,))
    billing = cursor.fetchone()

    cursor.execute("SELECT * FROM credentials WHERE userid=%s AND active=1", (user_id,))
    card = cursor.fetchone()

    cursor.close()
    conn.close()

    # Henter handlekurven for å vise produktene, deres individuelle priser og deres total pris til sammen
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

# Håndterer fullførte kjøp
@app.post("/checkout/complete")
def checkout_complete():
    # Henter relevant info som bruker id, handlekurven deres og produktlisten
    user_id = session.get("id")
    cart = session.get("cart", {})
    products = productlistings()

    # Sjekker om det ikke er en handlekurv tilgjengelig
    if not cart:
        return redirect("/cart")

    # Henter billing og bank info
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM billing WHERE userid=%s AND active=1", (user_id,))
    billing = cursor.fetchone()

    cursor.execute("SELECT id FROM credentials WHERE userid=%s AND active=1", (user_id,))
    card = cursor.fetchone()

    # Sjekker om det ikke finnes billing og bank info
    if not billing or not card:
        return redirect("/checkout")
    
    # Lager en lokal variabel for handlekurven (cart_items)
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

    # Lager en bestillings id for hele bestillingen, og kvitteringer for vert produkt i handlekurven forbundet med bestillings id-en
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

    # Tømmer handlekurven
    session["cart"] = []

    return render_template("ordersuccess.html", order_id=order_id)
```
---

## 8. Sikkerhet og pålitelighet

### Generelt
* Environment file (`.env`) brukt til oppbevaring av sensitive verdier.
* Miljøvariabler for databasepålogging,  databasestruktur og sikkerhets nøkkel
* Parameteriserte SQL-spørringer
* Validering av input fra bruker
* Feilhåndtering med `try/except`, `verdi sammenligning` og regulerte handlinger om hvise krav ikke møtes.

### Roller og tilgang
Applikasjonen benytter roller for å skille mellom brukertyper:
- **Kunde:** kan handle produkter og se egen profil
- **Admin:** har tilgang til administrasjonssider og produktstyring

Rollen lagres i session og brukes for å kontrollere tilgang til bestemte funksjoner.


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

Jeg lærte hvordan man bygger en fullstack-applikasjon med HTML, CSS, JS, PYTHON, Flask og Mariadb database.

### Hva fungerte bra?

Databasekobling og struktur fungerte stabilt.

### Hva var utfordrende?

Håndtering av relasjoner mellom tabeller og feilsøking i backend. Rettskriving i form av syntax og stuktur.

### Hva ville du gjort annerledes?

Jeg ville planlagt databasemodellen enda bedre før koding startet.

### Videre utvikling
Videre arbeid med prosjektet kunne inkludert:
- Fixing, forbedring og implementering frontend stuktur, funksjonalitet og responsivt design
- Bedre sikkerhet i form av sikkere lagring av betalingsdata og implementering av csrf tokens
- Fixing, forbedring og implementering av style, som css og kanskje js
