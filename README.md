# Flask-prosjekt -- Dokumentasjon
## 1. Forside
### Prosjekttittel: Nettbutikk
Navn: Alexander \
Klasse: 2IMI \
Dato: 11.11.2025

### Kort beskrivelse av prosjektet:
Prosjektet går ut på at jeg skal lage en nettbutikk, der jeg utnytter 3 eller flere tabeler fra en database.
Prosjektet går ut på å utvikle en nettbutikk ved hjelp av Flask og MariaDB. Applikasjonen benytter flere tabeller i databasen for å håndtere brukere, produkter, kjøp og betalingsinformasjon.

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

## 4. Prosjektstyring -- GitHub Projects (Kanban)

Prosjektet benyttet GitHub Projects med Kanban-tavle:

* **To Do**
* **In Progress**
* **Done**

### Refleksjon
Kanban-metoden gjorde det enklere å planlegge arbeidet, holde oversikt over fremdrift og prioritere oppgaver underveis i prosjektet.

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

---

## 7. Kodeforklaring
Her forklares hovedrutene i Flask-applikasjonen, for eksempel:

* `/login` – håndterer innlogging
* `/register` – registrering av brukere
* `/products` – viser produktkatalog
* `/checkout` – gjennomfører kjøp

---

## 8. Sikkerhet og pålitelighet

* `.env` brukt til sensitive verdier
* Miljøvariabler for databasepålogging
* Parameteriserte SQL-spørringer
* Validering av input fra bruker
* Feilhåndtering med `try/except`, `verdi sammenligning` og regulerte handlinger om hvise krav ikke møtes.

---

## 9. Feilsøking og testing
### Typiske feil

* Databaseforbindelse feilet
* Feil i SQL-spørringer
* Manglende validering av input

### Løsning

Feil ble løst ved bruk av logging, utskrift i konsoll og testing av SQL-spørringer direkte i databasen.

### Testmetoder

* Manuell testing av alle sider
* Testing med ulike brukere og roller

---

## 10. Konklusjon og refleksjon
Hva lærte du?:\
Hva fungerte bra?:\
Hva ville du gjort annerledes?:\
Hva var utfordrende?:
