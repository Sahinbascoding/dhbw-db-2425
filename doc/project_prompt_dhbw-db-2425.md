# 🔧 ChatGPT Prompt für Projekt DHBW-DB-2425 (Stand: April 2025)

Nutze diesen Prompt, um direkt mit mir an deinem Datenbankprojekt weiterzuarbeiten.

---

# 🧠 Projektüberblick

- **Projektname:** DHBW-DB-2425
- **Modul:** Datenbanksysteme (Teil 2)
- **Ziel:** Flask-Web-App zur Verwaltung und Analyse von Daten in MySQL & MongoDB
- **Tech-Stack:** Flask, SQLAlchemy, PyMySQL, pymongo, Bootstrap, HTML5

---


# 📁 Projektstruktur (Auszug)

```
├── app.py                       # Einstiegspunkt für Flask
├── .env                         # DB-Zugangsdaten (MySQL/MongoDB)
├── web_app/
│   ├── api/
│   │   ├── router.py            # Zentrale Route-Registrierung
│   │   └── routes/
│   │       ├── route_index.py   # Einzelrouten (z. B. add_data, convert, reports, etc.)
│   ├── infrastructure/
│   │   ├── config/config.py     # .env-Loader & Verbindungsstrings
│   │   └── database/helpers/    # DB-Hilfsfunktionen (MySQL, MongoDB)
├── src/tools/
│   ├── import_sql_db.py         # SQL-Importtool inkl. Fehlerbehandlung
│   ├── reset_mysql.py           # MySQL-Datenbank zurücksetzen
│   └── reset_mongo.py           # MongoDB-Datenbank löschen
├── src/sql/import/
│   ├── create_shema.sql         # Tabellenstruktur
│   ├── load_data.sql            # CSV-Import
│   ├── data_cleanup.sql         # Zusätze & Datenbereinigung
│   ├── update_fahrt.sql         # STR_TO_DATE Umwandlung (nur falls nötig)
├── src/sql/reports/             # SQL-Reports (durchschnittliche Geschwindigkeit, Fahreraktivität, Max-Speed)
├── data/                        # CSV + JSON-Daten
├── templates/                   # HTML-Templates für GUI
├── static/                      # CSS + Bilder
```

---

# ⚙️ Setup & Start

```bash
git clone https://github.com/Sahinbascoding/dhbw-db-2425.git
cd dhbw-db-2425
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

.env Datei anlegen:

```env
SECRET_KEY=deinSecret

MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=deinPasswort
MYSQL_DB_NAME=telematik

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB_NAME=telematik_nosql
```

Dann Web-App starten:

```bash
flask run
```

---

# 🛠️ Datenbank aufsetzen

✅ Per Web-GUI  
- 📥 **SQL importieren:** Button ruft `import_sql_db()` auf (führt alle SQL-Skripte aus)
- 🧹 **DB zurücksetzen:** Separate Buttons für `reset_mysql()` und `reset_mongo()`

✅ Alternativ manuell über CLI:
```bash
mysql -u root -p
CREATE DATABASE telematik;
EXIT;

mysql -u root -p telematik < src/sql/import/create_shema.sql
mysql -u root -p --local-infile=1 telematik < src/sql/import/load_data.sql
mysql -u root -p telematik < src/sql/import/data_cleanup.sql
```

---

# ✅ Aktueller Stand

- Vollständig modulare Flask-Web-App
- Fehlerfreier mehrfacher SQL-Import möglich (STR_TO_DATE nur wenn nötig)
- MongoDB-Konvertierung funktioniert (Flat & Embedded)
- Logging aller Konvertierungen in MySQL-Tabelle `Conversion_Log`
- Reports über Web-GUI abrufbar:
  - Ø Geschwindigkeit & Motortemperatur (März 2024)
  - Fahrer mit Fahrten der letzten 15 Monate
  - Maximale Geschwindigkeit je Fahrer
- JSON-Import über `/add-data` vorbereitet (unfall.json)
- `.env`-Konfiguration für portable Umgebungen
- Verbesserte Benutzerführung & Fehlerbehandlung

---

# 📋 Bisher erledigte Aufgaben (Teil 1-10)

- ✅ 1: MySQL-Datenimport und Aufbereitung (Transactions, Fehlerbehandlung)
- ✅ 2: Automatisiertes Setup über Web-GUI
- ✅ 3: Konvertierung von SQL-Tabellen zu MongoDB-Collections
- ✅ 4: Logging der Konvertierungen
- ✅ 5: Reports 1–3 fertiggestellt und integriert
- ✅ 6: JSON-Importmechanismus vorbereitet
- ✅ 7: Fehlerbehandlung für SQL-Import mehrmals verbessert
- ✅ 8: Trennung CSV/SQL-Import durch Anpassung der Trennzeichen gelöst

---

# ✅ Was du tun sollst

Wenn ich dir `config.py`, `router.py`, ein SQL-File, ein HTML-Template oder eine Route zeige:  
**Bearbeite direkt mit mir den Code.**  
Ich möchte keinen Kontext erklären müssen – du bist **voll im Projekt drin** 😎

Sag einfach „Bereit“, und ich leite den nächsten Schritt ein.

---
