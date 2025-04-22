from flask import redirect, url_for, flash
from src.tools.import_sql_db import import_sql

def import_sql_db():
    if import_sql():
        flash("SQL-Daten erfolgreich importiert.", "success")
    else:
        flash("Fehler beim SQL-Import.", "danger")
    return redirect(url_for("index"))
