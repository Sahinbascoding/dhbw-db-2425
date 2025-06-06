# Datei: web_app/api/routes/route_reports.py

import logging
import os
import sys
from flask import render_template, request, redirect, url_for
from infrastructure.database.helpers.helpers import get_mysql_connection

# Setup: Pfade sauber auflösen
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..', '..'))
sys.path.append(BASE_DIR)

# Reports-Verzeichnis
reports_path = os.path.join(BASE_DIR, 'src', 'sql', 'reports')

logger = logging.getLogger(__name__)

def reports():
    conn = get_mysql_connection()
    available_reports = {
        "fahrten_fahrer": "Anzahl der Fahrten pro Fahrer",
        "avg_speed_temp_march2024": "Ø Geschwindigkeit & Motortemperatur März 2024",
        "drivers_last_15_months": "Fahrer mit Fahrten in den letzten 15 Monaten",
        "max_speed_per_driver": "Maximale Geschwindigkeit pro Fahrer"
    }

    if request.method == 'POST':
        selected_report = request.form.get('report_type')
        return redirect(url_for('reports', report_type=selected_report))
    else:
        selected_report = request.args.get('report_type')
        page = request.args.get('page', 1, type=int)

    report_data = []
    cursor = conn.cursor()

    try:
        if selected_report == "fahrten_fahrer":
            query = """
                SELECT f.fahrerid, f.vorname, f.nachname, COUNT(ff.fahrtid) AS anzahl_fahrten
                FROM fahrer f
                JOIN fahrt_fahrer ff ON f.fahrerid = ff.fahrerid
                GROUP BY f.fahrerid, f.vorname, f.nachname;
            """
            cursor.execute(query)
            report_data = cursor.fetchall()
            report_data = [
                {"fahrerID": row[0], "vorname": row[1], "nachname": row[2], "anzahl_fahrten": row[3]}
                for row in report_data
            ]
            logger.info("Report 'fahrten_fahrer' loaded successfully.")

        elif selected_report == "avg_speed_temp_march2024":
            query_path = os.path.join(reports_path, 'avg_speed_temp_march2024.sql')
            with open(query_path, encoding="utf-8") as f:
                query = f.read()
            cursor.execute(query)
            report_data = cursor.fetchall()
            report_data = [
                {"durchschnitt_geschwindigkeit": row[0], "durchschnitt_motortemperatur": row[1]}
                for row in report_data
            ]
            logger.info("Report 'avg_speed_temp_march2024' loaded successfully.")

        elif selected_report == "drivers_last_15_months":
            query_path = os.path.join(reports_path, 'drivers_last_15_months.sql')
            with open(query_path, encoding="utf-8") as f:
                query = f.read()
            cursor.execute(query)
            report_data = cursor.fetchall()
            report_data = [
                {"fahrerID": row[0], "vorname": row[1], "nachname": row[2], "letzte_fahrt": row[3]}
                for row in report_data
            ]
            logger.info("Report 'drivers_last_15_months' loaded successfully.")

        elif selected_report == "max_speed_per_driver":
            query_path = os.path.join(reports_path, 'max_speed_per_driver.sql')
            with open(query_path, encoding="utf-8") as f:
                query = f.read()
            cursor.execute(query)
            report_data = cursor.fetchall()
            report_data = [
                {"fahrerID": row[0], "vorname": row[1], "nachname": row[2], "max_geschwindigkeit": row[3]}
                for row in report_data
            ]
            logger.info("Report 'max_speed_per_driver' loaded successfully.")

    except Exception as e:
        logger.error(f"Fehler beim Ausführen des Reports: {e}")

    finally:
        cursor.close()
        conn.close()

    # Paginierung
    items_per_page = 10
    total_items = len(report_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_data = report_data[start:end]

    return render_template(
        'reports.html',
        available_reports=available_reports,
        report_data=page_data,
        selected_report=selected_report,
        page=page,
        total_pages=total_pages
    )
