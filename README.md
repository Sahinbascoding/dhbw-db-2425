# DHBW-DB-2425 – README.md

## 📚 Project Overview  
**DHBW-DB_2023_24_App**  
**Version:** 1.0 (Final)

---

### 📝 Description
This project is a **Database Management Web Application** for MySQL and MongoDB. It enables importing, converting, resetting, and analyzing data through a user-friendly Flask interface.

---

### 🚀 Features
- ⚙️ **Table Conversion**: Migrate MySQL tables to MongoDB (flat or embedded).
- 📥 **Data Import (CSV/JSON)**: Import structured datasets into SQL and NoSQL.
- 🧹 **Database Reset**: Reset MySQL & MongoDB via one-click web buttons.
- ✏️ **Table Editing**: View and edit SQL tables directly via web.
- 📊 **Report Generation**: Predefined analytics on database contents.
- 🔄 **Dynamic Reload**: Refresh displayed table content via AJAX.

---

## 💻 Installation & Launch

```bash
git clone https://github.com/Sahinbascoding/dhbw-db-2425.git
cd dhbw-db-2425
python -m venv .venv
.venv\Scripts\activate        # (Windows)
pip install -r requirements.txt
```

> Erstelle anschließend eine `.env` Datei im Root-Verzeichnis:

```env
SECRET_KEY=dein-secret-key

MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=deinpasswort
MYSQL_DB_NAME=dein_db_name

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB_NAME=dein_mongo_db
```

Dann kannst du die Anwendung starten mit:

```bash
flask run
```

---

## 🧰 Datenbankverwaltung per Web-App

### Über die Benutzeroberfläche möglich:
- 🔁 **MySQL importieren:** Führt `create_shema.sql`, `load_data.sql`, `data_cleanup.sql` in dieser Reihenfolge aus.
- 🧹 **MySQL & MongoDB löschen:** Leere beide Datenbanken vollständig per Knopfdruck.
- 📦 **JSON hochladen:** Lade z. B. `unfall.json` manuell hoch und füge Inhalte ein.
- 🔄 **Konvertieren:** Wandle SQL-Daten in MongoDB-Collections um.

---

## ⚙️ Manuelle SQL-Nutzung

Falls gewünscht, kannst du die SQL-Dateien auch manuell ausführen:

```bash
mysql -u root -p
```

```sql
SET GLOBAL local_infile = 1;
EXIT;
```

```bash
mysql -u root -p < src/sql/import/create_shema.sql
mysql -u root -p --local-infile=1 < src/sql/import/load_data.sql
mysql -u root -p < src/sql/import/data_cleanup.sql
```

---

## 📂 Project Structure (Excerpt)

```
├── app.py                       # Entry point – startet Flask + Engine
├── .env                         # Lokale Konfigurationswerte
├── requirements.txt             # Benötigte Pakete
├── src/
│   ├── tools/                   # Import-/Reset-Skripte für Datenbanken
│   ├── sql/import/             # SQL-Dateien für Schema, Daten, Cleanup
├── web_app/
│   ├── api/router.py           # Zentrale Routing-Registrierung
│   ├── api/routes/             # Einzelrouten wie convert, import, reset...
│   ├── infrastructure/         # config.py + DB-Helper
│   ├── templates/              # HTML-Dateien (Jinja2)
│   ├── static/                 # CSS, Images
├── data/                       # CSV-/JSON-Beispieldaten
├── doc/                        # ER-Modell, Zeichnungen, Fortschritt
```

---

## ✅ Version & Team

**Version:** 1.0  
**Stand:** 22.04.2025  

**Contributors:**
- 🧑‍💻 Ata Sahinbas, Luis Kilic  
- 🏫 DHBW Stuttgart