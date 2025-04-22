# 🔧 ChatGPT Prompt für Projekt DHBW-DB-2425

**Bitte diesen Prompt in einem neuen Chat verwenden, um nahtlos an meinem Projekt weiterarbeiten zu können.**

---

## 🧠 Projektüberblick

- **Projektname:** DHBW-DB-2425
- **Ziel:** Webanwendung zur Verwaltung und Analyse von Daten in MySQL und MongoDB
- **Tech-Stack:** Flask, SQLAlchemy, PyMySQL, pymongo, Bootstrap

---

## 📁 Projektstruktur (Auszug)

```
├── app.py                    # Einstiegspunkt (setzt Flask, Engine, Logging auf)
├── src/
│   ├── sql/import/           # SQL-Dateien: create_shema.sql, load_data.sql, data_cleanup.sql, main_import.sql
├── web-app/
│   ├── api/routes/route.py   # Alle Flask-Routen
│   ├── infrastructure/       # config.py + DB-Helper
│   ├── templates/            # HTML (index, convert, reports, ...)
│   ├── static/               # Styles + Bilder
├── data/                     # JSON/CSV-Dateien
├── doc/                      # ER-Modell, TODOs etc.
```

---

## ⚙️ Setup

```bash
git clone ...
cd dhbw-db-2425
python -m venv .venv
.venv\Scripts\activate     # unter Windows
pip install -r requirements.txt
```

`.env` Datei mit DB-Zugangsdaten anlegen, danach:

```bash
flask run
```

**DB-Setup:**
```bash
mysql -u root -p --local-infile=1 telematik < src/sql/import/main_import.sql
```

---

## ✅ Aktueller Stand

- App läuft stabil, Templates & Static-Files korrekt eingebunden
- `main_import.sql` automatisiert den kompletten Datenbankaufbau
- Logging-Ausgaben wurden reduziert & durch `logging.info()` ersetzt
- Flask reagiert korrekt auf GET/POST, Debugging wurde vereinfacht

---

## 📋 To-Do (Teil 2)

- [ ] Konvertierung MySQL → MongoDB (auch embedded)
- [ ] Logging in `success_logs`-Tabelle (SQL)
- [ ] Report 1: Ø Geschwindigkeit & Temperatur März 2024
- [ ] Report 2: Fahrer mit Fahrten in den letzten 15 Monaten
- [ ] Report 3: Höchste Geschwindigkeit je Fahrer
- [ ] `unfall.json` in MongoDB einfügen
- [ ] Trigger-Logik bei Bearbeitungen in MySQL
- [ ] Stored Procedure zum Hinzufügen einer neuen Fahrt
- [ ] Alle Änderungen persistent in MySQL speichern

---

## ✅ Was du tun sollst

Wenn ich z. B. `app.py`, `route.py`, `config.py`, `main_import.sql` oder eine HTML-Datei zeige, arbeite bitte **direkt mit diesen Dateien weiter**. Du musst nichts vom Projekt mehr lernen – du bist ab jetzt voll involviert 😎

Sag mir einfach „Bereit“, wenn ich dir Dateien zeigen kann.
