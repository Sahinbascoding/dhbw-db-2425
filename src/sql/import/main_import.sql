-- #1: Aktiviere lokalen Dateiimport
SET GLOBAL local_infile = 1;

-- #2: Schema erstellen
SOURCE src/sql/import/create_shema.sql;

-- #3: Daten importieren (CSV-Dateien mit Transaktionen)
SOURCE src/sql/import/load_data.sql;

-- #4: Datenbereinigung und Beispieldaten ergänzen
SOURCE src/sql/import/data_cleanup.sql;