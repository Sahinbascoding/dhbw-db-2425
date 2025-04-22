# Datei: api/routes/route_reports.py

import logging
from flask import render_template, request, redirect, url_for
from infrastructure.database.helpers.helpers import get_mysql_connection

logger = logging.getLogger(__name__)

def reports():
    conn = get_mysql_connection()
    available_reports = {
        "fahrten_fahrer": "Anzahl der Fahrten pro Fahrer"
    }

    if request.method == 'POST':
        selected_report = request.form.get('report_type')
        return redirect(url_for('reports', report_type=selected_report))
    else:
        selected_report = request.args.get('report_type')
        page = request.args.get('page', 1, type=int)

    report_data = []
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

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
