# Datei: api/routes/route_generate_random_fahrt.py
import random
from flask import redirect, url_for, flash
from infrastructure.database.helpers.helpers import get_mysql_connection
from datetime import datetime, timedelta
import random
from datetime import datetime, timedelta
from flask import redirect, url_for, flash
from infrastructure.database.helpers.helpers import get_mysql_connection
import logging

logger = logging.getLogger(__name__)

def generate_random_fahrt():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        # Echte IDs holen
        cursor.execute("SELECT fahrzeugid FROM fahrzeug")
        fahrzeug_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT geraetid FROM geraet")
        geraet_ids = [row[0] for row in cursor.fetchall()]

        if not fahrzeug_ids or not geraet_ids:
            flash("⚠️ Keine Fahrzeuge oder Geräte in der Datenbank vorhanden!", "warning")
            return redirect(url_for('index'))

        fahrzeugid = random.choice(fahrzeug_ids)
        geraetid = random.choice(geraet_ids)
        startzeitpunkt = datetime.now() - timedelta(days=random.randint(0, 365))
        endzeitpunkt = startzeitpunkt + timedelta(minutes=random.randint(5, 120))
        route = f"Route {random.randint(1, 100)}"

        # Für Flash-Message vorbereiten
        call_statement = f"CALL AddFahrt({fahrzeugid}, {geraetid}, '{startzeitpunkt.strftime('%Y-%m-%d %H:%M:%S')}', '{endzeitpunkt.strftime('%Y-%m-%d %H:%M:%S')}', '{route}')"

        # Stored Procedure aufrufen
        cursor.callproc('AddFahrt', [
            fahrzeugid,
            geraetid,
            startzeitpunkt.strftime('%Y-%m-%d %H:%M:%S'),
            endzeitpunkt.strftime('%Y-%m-%d %H:%M:%S'),
            route
        ])

        conn.commit()
        cursor.close()
        conn.close()

        flash(f"✅ Zufällige Fahrt erfolgreich erstellt!<br><code>{call_statement}</code>", "success")
    except Exception as e:
        flash(f"❌ Fehler beim Erzeugen einer zufälligen Fahrt: {e}", "danger")

    return redirect(url_for('index'))