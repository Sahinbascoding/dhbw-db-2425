from flask import redirect, url_for, flash
from src.tools.initiate_db import initiate_db

def import_sql_db():
    try:
        initiate_db()
        flash("✅ SQL-Import und Setup abgeschlossen!", "success")
    except Exception as e:
        flash(f"❌ Fehler beim Initialisieren: {e}", "danger")
    return redirect(url_for("index"))
