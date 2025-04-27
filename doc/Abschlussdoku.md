📚 Abschlussdokumentation – Projekt Datenbankverwaltung

Stand: 27.04.2025

Teil 1: Aufgaben aus der ursprünglichen To-Do-Liste

1️⃣ ER-Modell als PDF

Erstellung eines vollständigen ER-Modells als PDF.

Darstellung aller Entitäten (fahrer, fahrzeug, fahrt, wartung, diagnose, gerät, usw.) sowie Primär- und Fremdschlüssel.

2️⃣ SQL-Skripte zur Erstellung des DB-Schemas (MySQL)

Entwicklung von create_shema.sql mit allen Tabellen und Constraints.

Besondere Anpassung: fahrtid als AUTO_INCREMENT, aber Import der Zeitangaben zunächst als VARCHAR.

Teil 2: Aufgaben aus der ursprünglichen To-Do-Liste

3️⃣ Import aller Daten in das MySQL-Schema + Datenbereinigung

CSV-Import via load_data.sql.

Umwandlung von Datumstexten zu DATETIME via update_fahrt.sql.

Vollständige Integration der SQL-Skripte in den automatisierten Importprozess.

4️⃣ Alle Importe innerhalb von Transaktionen

Alle Importschritte laufen in Transaktionen (BEGIN / COMMIT).

Fehlerhafte Imports lösen automatische Rollbacks aus.

5️⃣ Lauffähige App

Web-App umgesetzt mit Flask (web_app/).

Startpunkt app.py, zentrale Routenregistrierung in api/router.py.

Verwendung von .env für Konfigurationswerte.

6️⃣ Konvertierung der Tabellen nach MongoDB

Implementierung von convert_to_mongodb().

Flat- und Embedded-Konvertierung.

Beispiel: fahrer_mit_fahrten eingebettete Collection.

7️⃣ Logging von Konvertierungen (MySQL Log-Tabelle)

Automatische Protokollierung der Konvertierungen in conversion_log.

Felder: source_table, target_collection, status, duration_seconds, timestamp.

8️⃣ Report 1: Durchschnittliche Geschwindigkeit und Motortemperatur (März 2024)

Erstellung des Reports in avg_speed_temp_march2024.sql.

Zugriff über das Web-Frontend unter /reports.

9️⃣ Report 2: Fahrer, die in den letzten 15 Monaten aktiv waren

SQL-Datei drivers_last_15_months.sql mit Vergleich über DATE_SUB(CURDATE(), INTERVAL 15 MONTH).

🚀 Report 3: Maximale Geschwindigkeit je Fahrer

Höchste Geschwindigkeit je Fahrer ermittelt über max_speed_per_driver.sql.

Verknüpfung über fahrtid und fahrzeugparameter.

📦 Hinzufügen der Collection unfall.json in MongoDB

Zusätzliche Route /add-data für das Hochladen von JSON-Dateien.

Direkte Speicherung der Daten in MongoDB.

🔄 Editieren von Tabellen wird in eine Changelog-Tabelle getriggert

Jeder Änderungsvorgang wird automatisch über Trigger in changelog eingetragen.

Separate Trigger-Skripte für jede Tabelle.

🔢 Stored Procedure zum Hinzufügen einer neuen Fahrt

Implementierung der Stored Procedure AddFahrt.

Verwaltung über add_fahrt_procedure.sql.

🔄 Änderungen werden immer persistent gespeichert

Update-Route /update-row schreibt Änderungen direkt in die MySQL-Datenbank.

Sicherstellung über db.commit().

Zusätzliche von uns entwickelte Features

🛋️ Strukturierte Tools und Scripts

Einheitliche Verwaltung aller Skripte in src/tools/.

Einheitliche Pfadstruktur über BASE_DIR und CURRENT_DIR für alle Skripte.

🚧 Verbesserte Fehlerbehandlung

Fehler bei Import, Update, Konvertierung werden abgefangen und mit flash() visualisiert.

🏋️ Komplettintegration Trigger & Procedures

Alle Trigger- und Stored Procedure Skripte werden zentral beim Import aktiviert.

🔹 Design, Logik und Implementierung der Webapp-Buttons (Sonderaufgabe)

Implementierung einer zusätzlichen Button-Zeile im Web-Frontend:

SQL-Daten importieren: Läuft import_sql() und führt alle SQL-Skripte automatisch aus.

MySQL löschen: Setzt die MySQL-Datenbank zurück und erstellt sie neu.

MongoDB löschen: Leert alle MongoDB-Collections.

Zufällige Fahrt generieren: Erzeugt neue Testdatensätze.

Alle Buttons sind über Flask-Routen angebunden (/import-sql, /reset-mysql, /reset-mongodb, /generate-random-drive).

Jede SQL-bezogene Funktion hat:

Ein separates SQL-Skript im Ordner src/sql/

Eine zugehörige Python-Funktion, die das Skript ausführt.

📋 Zusammenfassung

Alle Aufgaben aus der Aufgabenstellung abgeschlossen ✅

Zusätzliche sinnvolle Features wurden integriert.

Saubere, modulare Codestruktur.

Volle Persistenz und Konsistenz der Daten erreicht.

🚀 Projektstatus: Abgeschlossen!

