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
| customers | id | INT | Primærnøkkel | 
| customers | name | VARCHAR(255) | Navn | 
| customers | address | VARCHAR(255) | Adresse |

SQL-eksempel:

CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  address VARCHAR(255)
);

## 6. Programstruktur
projectnavn /
  ├ static/
  │    ├──css/
  │    │  └──useradministration.html
  │    ├──images/
  │    └──js/
  │      └──useradministration.html
  ├── templates/
  │    ├──index.html
  │    ├──layout.html
  │    ├──profilepage.html
  │    ├──products.html
  │    └──useradministration.html
  ├── .env
  ├── .gitingnore
  ├── app.py
  ├── functions.py
  └── README.md
Databasestrøm:

HTML → Flask → MariaDB → Flask → HTML-tabell

## 7. Kodeforklaring
Forklar ruter og funksjoner (kort).

## 8. Sikkerhet og pålitelighet
.env\
Miljøvariabler\
Parameteriserte spørringer\
Validering\
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

## 11. Kildeliste
w3schools\
flask.palletsprojects.com
