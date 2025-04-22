-- 🟡 Aktiviere lokalen Dateiimport (falls nötig)
-- In MySQL-Shell ausführen, falls lokale Dateiimporte deaktiviert sind:
-- SET GLOBAL local_infile = 1;

-- #TODO 1: Schema erstellen
SOURCE TEIL1/create_shema.sql;
-- ✅ Schema erstellt

-- #TODO 2: Daten importieren (CSV-Dateien mit Transaktionen)
SOURCE TEIL2/load_data.sql;
-- ✅ CSV-Daten erfolgreich geladen

-- #TODO 3: Datenbereinigung und Beispieldaten ergänzen
SOURCE TEIL2/data_cleanup.sql;
-- ✅ Cleanup durchgeführt (Daten ergänzt + korrigiert)

-- 🟢 Alle Import-Schritte erfolgreich abgeschlossen!
