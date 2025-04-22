
# 🚗 DHBW-Datenbankprojekt – Telematikdatenverwaltung
# 1. DB löschen & neu erstellen
mysql -u root -p
> DROP DATABASE IF EXISTS telematik;
> CREATE DATABASE telematik;
> EXIT;

# 2. Schema importieren (mit korrekter Datei)
mysql -u root -p telematik < TEIL1/create_shema.sql

# 3. Daten importieren (korrekt mit --local-infile)
mysql --local-infile=1 -u root -p telematik < TEIL2/load_data.sql

# 4. Optional: Daten bereinigen
mysql -u root -p telematik < TEIL2/data_cleanup.sql

## 📦 Schnellstart

### 🛠️ Datenbank erstellen und füllen (empfohlen)

```bash
cd C:\appldev\dhbw-db-2425
mysql -u root -p --local-infile=1 telematik < main_import.sql
```

---

### ⚙️ Alternativ: Schritte manuell ausführen

## 1 – Schema erstellen

```bash
cd C:\appldev\dhbw-db-2425
```

Tabellen anlegen:

```bash
mysql -u root -p telematik < TEIL1\create_schema.sql
```

---

## 2 – local_infile aktivieren

Unterstützung für lokale Dateien aktivieren:

```bash
mysql -u root -p --local-infile=1
```

In MySQL-Shell:

```sql
SET GLOBAL local_infile = 1;
EXIT;
```

---

## 3 – CSV-Daten importieren

```bash
mysql -u root -p --local-infile=1 telematik < TEIL2\load_data.sql
```

⚠️ Hinweis: Die Dateien `fahrt.json` und `unfall.json` müssen **manuell in MongoDB Compass** oder per Python importiert werden – sie sind **nicht Bestandteil des SQL-Imports**.

---

## ✅ Ergebnis prüfen (optional)

```bash
mysql -u root -p
```

In MYSQL-Shell:

```sql
USE telematik;
SHOW TABLES;
SELECT COUNT(*) FROM fahrzeug;
```

---
