# Fortschrittsbericht – Teilaufgaben 1 bis 4

**Stand:** 22.04.2025

## ✅ Abgeschlossene Teilaufgaben

---

### 🧩 1. Import aller Daten in das MySQL-Schema
- Implementierung und Ausführung von SQL-Skripten (`create_schema.sql`, `load_data.sql`, `data_cleanup.sql`)
- Import aller CSV-Dateien mit `--local-infile=1` erfolgreich abgeschlossen
- Tabellenanzahl und Datenmengen im MySQL-Informationsschema geprüft

---

### 🔄 2. Alle Importe innerhalb von Transaktionen
- Importlogik in `load_data.sql` wurde in Transaktionen gekapselt
- Datenimport bricht bei Fehlern vollständig ab
- Konsistenz der Daten wird durch `START TRANSACTION`, `COMMIT`, `ROLLBACK` sichergestellt

---

### 🧪 3. Lauffähige Web-App
- Struktur: Flask-App mit `app.py`, Routenmodul (`routes/route.py`), Templates, statische Ressourcen
- Verwendung von `.env` für sensible Konfigurationen
- GUI-Routen: `/`, `/convert`, `/add-data`, `/reports`, `/view-table`, `/database-stats`
- Erfolgreicher Start via `flask run`
- Logging und SQLAlchemy angebunden

---

### ☁️ 4. Konvertierung der Tabellen nach MongoDB
- Konvertierungsfunktion implementiert:
  - `convert_single_table(table_name, engine, db)`
  - `convert_embedded(tables, engine, db)`
- Trennung in:
  - Einzelne MongoDB-Collections
  - Embedded-Collection `fahrer_mit_fahrten`
- Konfigurierbar über Web-Oberfläche `/convert`
- Validierung mit `compare_counts.py`: Datenmenge in MySQL = MongoDB
- Pfadkorrekturen & Strukturvervollständigung in `helpers.py` und `config.py`

---

## 📌 Nächste Aufgabe:
- Hochladen und Einfügen von JSON-Dateien über `/add-data` (z. B. `unfall.json`)
