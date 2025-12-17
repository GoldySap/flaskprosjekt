# Flask-prosjekt -- Dokumentasjon
## 1. Forside
### Prosjekttittel: Nettbutikk
Navn: Alexander \
Klasse: 2IMI \
Dato: 11.11.2025

### Kort beskrivelse av prosjektet:
Prosjektet går ut på at jeg skal lage en nettbutikk, der jeg utnytter 3 eller flere tabeler fra en database.

## 2. Systembeskrivelse
### Formål med applikasjonen:
Applikasjonen skal være en nettbutikk som inneholder en product katalog, en login og registrering for kontoer, en handlekurv for valgte producter, en kvitering av kjøp som kjøpe historikk, og bruker instilinger.

### Brukerflyt:
Brukeren starter på hjemmesiden der de kan bruke navbaren til å gå til de forskjellige sidene, som å logge inn, profil siden deres, gå til product katalogen, gå til deres handlekurv og retunere tilbake til hjemmesiden.

### Teknologier brukt:
Python / Flask\
MariaDB\
HTML / CSS / JS / JQuery\

## 3. Server-, infrastruktur- og nettverksoppsett
### Servermiljø
Server: Rasberry PI 
Operativsystem: Ubuntu

### Nettverksoppsett:
Nettverksdiagram:\
<img width="424" height="384" alt="Diagram" src="https://github.com/user-attachments/assets/8722f083-4119-4ba0-b96c-180cca1bea69" />\
IP-adresser: 10.200.14.20\
Porter:\
Brannmurregler:

Eksempel:
Klient → MariaDB
Tjenestekonfigurasjon
systemctl / Supervisor\
Filrettigheter\
Miljøvariabler

## 4. Prosjektstyring -- GitHub Projects (Kanban)
To Do / In Progress / Done\
Issues\
Skjermbilde (valgfritt)
Refleksjon: Hvordan hjalp Kanban arbeidet?:
Kanban har gjort det enkelt å planlege og holde styr å det som skal gjøres, er i progression eller ferdig.

## 5. Databasebeskrivelse
Databasenavn:nettbutikk

<img width="878" height="603" alt="Nettbutikk_Diagram" src="https://github.com/user-attachments/assets/a543641c-a9c9-46d3-aef0-c72f7029c825" />

Tabeller:
| Tabell | Felt | Datatype | Beskrivelse | 
|--------|------|----------|-------------| 
| users | id | INT | Primærnøkkel | 
| users | email | VARCHAR(255) | Navn | 
| users | password | VARCHAR(255) | Adresse |
| users | active | BOOL | Navn | 
| users | role | VARCHAR(255) | Adresse |

| Tabell | Felt | Datatype | Beskrivelse | 
|--------|------|----------|-------------| 
| products | id | INT | Primærnøkkel | 
| products | name | VARCHAR(255) | Navn | 
| products | address | VARCHAR(255) | Adresse |

| Tabell | Felt | Datatype | Beskrivelse | 
|--------|------|----------|-------------| 
| credentials | id | INT | Primærnøkkel | 
| credentials | name | VARCHAR(255) | Navn | 
| credentials | address | VARCHAR(255) | Adresse |

| Tabell | Felt | Datatype | Beskrivelse | 
|--------|------|----------|-------------| 
| billing | id | INT | Primærnøkkel | 
| billing | name | VARCHAR(255) | Navn | 
| billing | address | VARCHAR(255) | Adresse |

| Tabell | Felt | Datatype | Beskrivelse | 
|--------|------|----------|-------------| 
| recipt | id | INT | Primærnøkkel | 
| recipt | name | VARCHAR(255) | Navn | 
| recipt | address | VARCHAR(255) | Adresse |

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
  securitycode INT NOT NULL, \
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

## 7. Kodeforklaring
Forklar ruter og funksjoner (kort).

## 8. Sikkerhet og pålitelighet
.env: Ja \
Miljøvariabler: ja \
Parameteriserte spørringer: ja\
Validering: Ja \
Feilhåndtering: delvis

## 9. Feilsøking og testing
Typiske feil:\
Hvordan du løste dem:\
Testmetoder:

## 10. Konklusjon og refleksjon
Hva lærte du?:\
Hva fungerte bra?:\
Hva ville du gjort annerledes?:\
Hva var utfordrende?:
