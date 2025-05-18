## 🛠️ Manuelle Ausführung (ohne Web-Oberfläche)

Alle Funktionen der Web-App lassen sich auch manuell über das Terminal oder direkt in der MySQL-Shell ausführen – z. B. für Tests, Debugging oder Automatisierung.

---

### 🔹 1. MySQL öffnen & vorbereiten

```bash
mysql --local-infile=1 -u root -p
```

```sql
SET GLOBAL local_infile = 1;
USE telematik;
```

---

### 🔹 2. SQL-Skripte in richtiger Reihenfolge ausführen

```sql
SOURCE src/sql/import/create_shema.sql;
SOURCE src/sql/import/load_data.sql;
SOURCE src/sql/import/update_fahrt.sql;
SOURCE src/sql/import/data_cleanup.sql;
```

---

### 🔹 3. Reports manuell anzeigen

```sql
SOURCE src/sql/reports/avg_speed_temp_march2024.sql;
SOURCE src/sql/reports/drivers_last_15_months.sql;
SOURCE src/sql/reports/max_speed_per_driver.sql;
```

---

### 🔹 4. Trigger testen (Changelog)

#### Trigger aktivieren:

```sql
SOURCE src/sql/triggers/beschleunigung_trigger.sql;
```

#### Beispielwert ändern:

```sql
SELECT * FROM beschleunigung LIMIT 1;

UPDATE beschleunigung
SET x_achse = x_achse + 1.0
WHERE beschleunigungid = 42;
```

#### Changelog anzeigen:

```sql
SELECT * FROM changelog
WHERE table_name = 'beschleunigung'
ORDER BY changed_at DESC
LIMIT 5;
```

---

### 🔹 5. Fahrt mit Stored Procedure hinzufügen

#### Stored Procedure aktivieren:

```sql
SOURCE src/sql/procedures/add_fahrt_procedure.sql;
```

#### Vorhandene IDs prüfen:

```sql
SELECT fahrzeugid FROM fahrzeug LIMIT 5;
SELECT geraetid FROM geraet LIMIT 5;
```

#### Neue Fahrt einfügen:

```sql
CALL AddFahrt(1, 101, '2024-04-01 08:00:00', '2024-04-01 09:00:00', 'Teststrecke A');
```

#### Kontrolle:

```sql
SELECT * FROM fahrt ORDER BY fahrtid DESC LIMIT 5;
```

---

### 🔹 6. MySQL → MongoDB konvertieren

#### Vorbereitung:

```powershell
$env:PYTHONPATH="$PWD\web_app"
```

#### Vollständige Konvertierung aller Tabellen:

```powershell
python -c "from src.no_sql.convert_to_mongo import convert_to_mongodb; from infrastructure.config.config import MYSQL_TABLES; convert_to_mongodb(MYSQL_TABLES, embed=False)"
```

#### Nur fahrer → fahrten einbetten:

```powershell
python -c "from src.no_sql.convert_to_mongo import convert_to_mongodb; convert_to_mongodb(['fahrer', 'fahrt', 'fahrt_fahrer'], embed=True)"
```

---

### 🔹 7. JSON-Dateien in MongoDB importieren

```powershell
python -c "from src.no_sql.insert_json_to_mongo import insert_json_to_mongo; insert_json_to_mongo('data/unfall.json', 'unfall')"
```

---

### 🔹 8. Datenbanken zurücksetzen

#### MySQL:

```powershell
python -c "from src.tools.reset_db import reset_mysql; reset_mysql()"
```

#### MongoDB:

```powershell
python -c "from src.tools.reset_db import reset_mongo; reset_mongo()"
```
