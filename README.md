# 🧰 Datenbankverwaltung per Web-App

Diese Web-Anwendung ermöglicht das Arbeiten mit zwei Datenbankmodellen (MySQL und MongoDB) – **ganz ohne manuelle Skriptausführung**. Alle Aufgaben lassen sich bequem über die Benutzeroberfläche mit einem Klick ausführen.

## 🌐 Funktionen der Web-App

### 🔄 Datenimport (SQL → MySQL)

Beim Klick auf **„SQL-Daten importieren“** wird `initiate_db.py` ausgeführt. Dieses ruft folgende Module auf:

1. **`enable_local_infile.py`**  
   Aktiviert das Laden lokaler Daten (`enable_local_infile()`).

2. **`import_sql_db.py`**  
   Führt folgende SQL-Skripte aus – in dieser Reihenfolge:
   - `create_shema.sql`
   - `load_data.sql`
   - `update_fahrt.sql`
   - `data_cleanup.sql`

3. **`activate_triggers.py`**  
   Aktiviert Trigger für das Logging in der Changelog-Tabelle.

4. **`activate_procedures.py`**  
   Aktiviert Stored Procedures zum späteren Hinzufügen von Fahrten.

---

### 🔁 Konvertierung: MySQL → MongoDB

- **„In MongoDB konvertieren“** ruft `convert_to_mongo.py` auf.
- Daten werden in MongoDB übertragen.
- Optional: Erstellung einer **embedded Collection** bei Tabellenauswahl.
- Die im `create_shema.sql` definierte **Log-Tabelle** wird dabei automatisch mit Konvertierungsdaten gefüllt.

---

### 📊 Reports (SQL-Abfragen)

Durch Auswahl eines Reports werden entsprechende SQL-Dateien ausgeführt:
- `avg_speed_temp_march2024.sql`
- `drivers_last_15_months.sql`
- `max_speed_per_driver.sql`

---

### 📥 JSON-Daten importieren (MongoDB)

- Beim Klick auf **„Daten importieren“** kann z. B. `unfall.json` hochgeladen und über `insert_json_to_mongo.py` in MongoDB eingefügt werden.

---

### 📝 Trigger & Changelog

- Beim Editieren einer MySQL-Tabelle wird automatisch ein zugehöriger Trigger ausgeführt (`Tabelle-Namen_trigger.sql`), der Änderungen in einer **Changelog-Tabelle** protokolliert.

---

### 🧪 Zufällige Fahrt generieren

- Per Knopfdruck wird in der Route `route_generate_random_fahrt.py` mithilfe einer Stored Procedure (`add_fahrt_procedure.sql`) eine Fahrt mit Zufallswerten erzeugt.

---

## ➕ Extras

- **MySQL-Import per Button**: `initiate_db.py` erledigt alles automatisch.
- **MySQL/MongoDB löschen**: Per Button werden `reset_mysql()` bzw. `reset_mongo()` aufgerufen.
- **Zufällige Fahrt erstellen**: Siehe oben bei „Zufällige Fahrt generieren“.

---

## ⚙️ Voraussetzungen

### 🔑 MySQL aktivieren

```powershell
Get-Service | Where-Object { $_.Name -like "*mysql*" }
net start mysql
# oder
net start MySQL80
```

### 🟢 MongoDB aktivieren

```powershell
Get-Service | Where-Object { $_.Name -like "*mongo*" }
net start MongoDB
# oder
net start MongoDBServer
```

### 🐍 Python

[Download Python](https://www.python.org/downloads/)

---

### 🗄️ MySQL

MySQL & MySQL Shell müssen installiert sein:  
- [MySQL Community Server](https://www.mysql.com/downloads/)  
- [MySQL Shell](https://dev.mysql.com/downloads/shell/)

### 🍃 MongoDB

MongoDB & MongoDB Shell müssen installiert sein:  
- [MongoDB Community Edition](https://www.mongodb.com/try/download/community)  
- [MongoDB Shell](https://www.mongodb.com/try/download/shell)

---

## 💻 Installation & Start

### 🔧 Projekt klonen

```powershell
git clone https://github.com/Sahinbascoding/dhbw-db-2425.git
cd dhbw-db-2425
```

### 🧪 Virtuelle Umgebung erstellen & aktivieren

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 📦 Abhängigkeiten installieren

```powershell
pip install -r requirements.txt
```

---

### 🛠️ `.env`-Datei im Root-Verzeichnis erstellen

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

---

### ▶️ App starten

```powershell
flask run
```

---




## ⚙️ Manuelle SQL-Nutzung

Falls gewünscht, können die MYSQL und Python-files auch manuell ausgeführt werden.
Dafür das README_Manual.md lesen.



## ✅ Version & Team

**Version:** 1.0  
**Stand:** 18.05.2025

**Contributors:**
- 🧑‍💻 Ata Sahinbas, Luis Kilic  