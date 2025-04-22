
# 🔧 ChatGPT Prompt für Projekt DHBW-DB-2425 (Stand: April 2025)

**Nutze diesen Prompt, um direkt mit mir an deinem Datenbankprojekt weiterzuarbeiten.**

---

## 🧠 Projektüberblick

- **Projektname:** DHBW-DB-2425  
- **Modul:** Datenbanksysteme (Teil 2)  
- **Ziel:** Flask-Web-App zur Verwaltung und Analyse von Daten in MySQL & MongoDB  
- **Tech-Stack:** Flask, SQLAlchemy, PyMySQL, pymongo, Bootstrap, HTML5

---

## 📁 Projektstruktur (Auszug)

```
├── app.py                       # Einstiegspunkt für Flask
├── .env                         # DB-Zugangsdaten (MySQL/MongoDB)
├── web_app/
│   ├── api/
│   │   ├── router.py            # Zentrale Route-Registrierung
│   │   └── routes/
│   │       ├── route_index.py   # Einzelrouten (z. B. add_data, convert, etc.)
│   ├── infrastructure/
│   │   ├── config/config.py     # .env-Loader & Verbindungsstrings
│   │   └── database/helpers/
├── src/tools/
│   ├── import_sql_db.py         # Führt 3 SQL-Dateien einzeln aus
│   ├── reset_mysql.py           # MySQL-Datenbank zurücksetzen
│   └── reset_mongo.py           # MongoDB-Datenbank löschen
├── src/sql/import/
│   ├── create_shema.sql         # Tabellenstruktur
│   ├── load_data.sql            # CSV-Import
│   └── data_cleanup.sql         # Zusätze & Datenbereinigung
├── data/                        # CSV + JSON-Daten
├── templates/                   # HTML-Templates
├── static/                      # CSS + Bilder
```

---

## ⚙️ Setup & Start

```bash
git clone https://github.com/Sahinbascoding/dhbw-db-2425.git
cd dhbw-db-2425
python -m venv .venv
.venv\Scripts\activate              # (Windows)
pip install -r requirements.txt
```

`.env` Datei anlegen:

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

## 🧰 Datenbank aufsetzen

### ✅ Per Web-GUI  
- 📥 **SQL importieren:** Button „📥 SQL-Daten importieren“ ruft `import_sql_db()` auf  
- 🧹 **DB zurücksetzen:** Buttons für `reset_mysql()` & `reset_mongo()`  

### ⚙️ Alternativ manuell

```bash
mysql -u root -p
```

```sql
CREATE DATABASE telematik;
EXIT;
```

```bash
mysql -u root -p telematik < src/sql/import/create_shema.sql
mysql -u root -p --local-infile=1 telematik < src/sql/import/load_data.sql
mysql -u root -p telematik < src/sql/import/data_cleanup.sql
```

---

## ✅ Aktueller Stand

- Vollständig modulare Flask-Web-App mit strukturierter Routenarchitektur
- MySQL-Import über GUI ausführbar – kein manuelles Terminal nötig
- MongoDB-Konvertierung funktioniert (inkl. embedded Documents)
- Alle Datenbankverbindungen `.env`-gesteuert (Projekt ist portierbar)
- Logging und Fehlerausgabe stabilisiert

---

## 📋 Offene To-Dos (Teil 2)

- [ ] Trigger und Logging in MySQL bei Update-Operationen
- [ ] Stored Procedure zur Fahrt-Erzeugung (mit Parametern)
- [ ] Mehrere Reports (TOP N-Fahrer, Durchschnittswerte etc.)
- [ ] MongoDB: `unfall.json` korrekt integrieren
- [ ] Verbesserte Benutzerführung in der Oberfläche

---

## ✅ Was du tun sollst

Wenn ich dir `config.py`, `router.py`, ein SQL-File, HTML oder eine Route zeige:  
**Bearbeite direkt mit mir den Code.**  
Ich möchte keinen Kontext erklären müssen – du bist **voll im Projekt drin** 😎

---

Sag einfach „Bereit“, und ich leite den nächsten Schritt ein.
