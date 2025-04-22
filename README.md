# DHBW-DB-2425 – README.md

## 📚 Project Overview  
**DHBW-DB_2023_24_App**  
**Version:** 0.1 

---
### 📝 Description
This project is a **Database Management Web Application** for MySQL and MongoDB. It provides features such as table conversion, data import, and report generation.

### 🚀 Features:
- ⚙️ **Table Conversion:** Convert tables to MongoDB (embedded or flat).
- 📥 **Data Import:** Upload and insert JSON documents.
- 📊 **Report Generation:** Run custom SQL reports.
- ✏️ **Table Editing:** Modify table entries with automatic change logging.
- 🔄 **Reload Functionality:** Refresh data tables.

---
## 💻 Installation & Start

```bash
git clone https://github.com/Sahinbascoding/dhbw-db-2425.git
cd dhbw-db-2425
python -m venv .venv
.venv\Scripts\activate        # (Windows)
pip install -r requirements.txt
```

Erstelle dann eine `.env` Datei mit den nötigen Variablen (MySQL/MongoDB-Verbindung usw.).

```bash
flask run
```

Zum Abschluss:  
Erstelle die Datenbank anschließend entweder **automatisch** mit `main_import.sql` oder **manuell** über die drei SQL-Schritte.

---
## 🧰 Datenbank erstellen

### ✅ Automatisch 
```bash
mysql -u root -p --local-infile=1 telematik < src/sql/import/main_import.sql

```

### ⚙️ Manuell  
Falls nötig zuerst:
```bash
mysql -u root -p
```
```sql
SET GLOBAL local_infile = 1;
EXIT;
```
Dann:
```bash
mysql -u root -p telematik < src/sql/import/create_shema.sql
mysql -u root -p --local-infile=1 telematik < src/sql/import/load_data.sql
mysql -u root -p telematik < src/sql/import/data_cleanup.sql
```

---
## 📂 Project Structure
```
├── app.py
├── .env
├── requirements.txt
├── README.md
├── .gitignore
│
├── src
│   ├── sql
│   │   ├── import
│   │   │   ├── create_shema.sql
│   │   │   ├── load_data.sql
│   │   │   ├── data_cleanup.sql
│   │   │   ├── main_import.sql
│   │   ├── report/
│   ├── no_sql/
│
├── web-app
│   ├── api/routes
│   │   └── route.py
│   ├── infrastructure
│   │   ├── config/config.py
│   │   └── database/helpers/helpers.py
│   ├── static
│   │   ├── images/dhbw_logo.png
│   │   └── styles.css
│   └── templates
│       ├── index.html
│       ├── layout.html
│       ├── add_data.html
│       ├── convert.html
│       ├── reports.html
│       ├── select_table.html
│       ├── view_table.html
│
├── data
│   ├── fahrzeug.csv
│   ├── unfall.json
│
├── doc
│   ├── ER-Modell.drawio / .png / .pdf
│   ├── TODO
```

---
### 📈 Version
This README uses the version displayed from the project: **Version 0.1**.

### 💡 Contributors
- 🧑‍💻 Ata Sahinbas, Luis Kilic
- 🏫 Organization: DHBW Stuttgart