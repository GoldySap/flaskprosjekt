# Flask-prosjekt -- Dokumentasjon
## 1. Forside
Prosjekttittel: Nettbutikk \
Navn: Alexander \
Klasse: 2IMI \
Dato: 11.112025

Kort beskrivelse av prosjektet: \
Prosjektet går ut på at jeg skal lage en nettbutikk, der jeg utnytter 3 eller flere tabeler fra en database.

## 2. Systembeskrivelse
Formål med applikasjonen: \
Buttiken skal ha en product katalog, man skal kunne lage en konto, lege producter i din handlevågn, så skal en kvitering lages av kjøpet og loges under kjøp historikk.

Brukerflyt: \
Brukeren starter på hjemmesiden som velkommer dem og viser et lite utvalg av dagens varer, så via navbaren skal de kunne navigere til andre deler av siden som for eksempel en produkt katalog og lage en konto for å lege til informasjonen derer og skape en kjøpe historikk.

Teknologier brukt: \
Python / Flask\
MariaDB\
HTML / CSS / JS\
(valgfritt) Docker / Nginx / Gunicorn / Waitress osv.

## 3. Server-, infrastruktur- og nettverksoppsett
Servermiljø
F.eks.: Ubuntu VM, Docker, fysisk server.

Nettverksoppsett
Nettverksdiagram
IP-adresser\
Porter\
Brannmurregler
Eksempel:

Klient → Waitress → MariaDB
Tjenestekonfigurasjon
systemctl / Supervisor\
Filrettigheter\
Miljøvariabler

## 4. Prosjektstyring -- GitHub Projects (Kanban)
To Do / In Progress / Done\
Issues\
Skjermbilde (valgfritt)
Refleksjon: Hvordan hjalp Kanban arbeidet?

## 5. Databasebeskrivelse
Databasenavn:nettbutikk

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
  │    │  └──useradministration.html \
  │    ├──images \
  │    └──js \
  │       ├──layout.js \
  │       └──loginregister.js \
  ├── templates \
  │    ├──index.html \
  │    ├──layout.html \
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

HTML → Flask → MariaDB → Flask → HTML-tabell

## 7. Kodeforklaring
Forklar ruter og funksjoner (kort).

## 8. Sikkerhet og pålitelighet
.env \
Miljøvariabler \
Parameteriserte spørringer \
Validering \
Feilhåndtering

## 9. Feilsøking og testing
Typiske feil\
Hvordan du løste dem\
Testmetoder

## 10. Konklusjon og refleksjon
Hva lærte du?\
Hva fungerte bra?\
Hva ville du gjort annerledes?\
Hva var utfordrende?
