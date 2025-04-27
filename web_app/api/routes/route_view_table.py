# Datei: api/routes/route_view_table.py
import os
import subprocess
import platform
from infrastructure.config.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME
from flask import render_template, request, redirect, url_for
from sqlalchemy import MetaData, text
import logging
from app import mysql_engine

# BASE_DIR sauber ermitteln
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

logger = logging.getLogger(__name__)

def run_trigger_for_table(selected_table):
    trigger_dir = os.path.join(BASE_DIR, "src", "sql", "triggers")
    trigger_filename = f"{selected_table}_trigger.sql"
    trigger_filepath = os.path.join(trigger_dir, trigger_filename)

    if not os.path.exists(trigger_filepath):
        print(f"❌ Kein Trigger-SQL-File gefunden für Tabelle: {selected_table}")
        return

    mysql_command = [
        "mysql",
        "-h", MYSQL_HOST,
        "-u", MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        MYSQL_DB_NAME
    ]

    try:
        with open(trigger_filepath, "rb") as sql_file:
            subprocess.run(mysql_command, stdin=sql_file, check=True)
        print(f"✅ Trigger für Tabelle '{selected_table}' erfolgreich ausgeführt.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Ausführen des Triggers für Tabelle '{selected_table}': {e}")
        return  # Frühzeitig abbrechen, damit Flush nicht trotzdem ausgeführt wird

    try:
        # Danach: FLUSH TABLES sauber ausführen
        with mysql_engine.connect() as connection:
            connection.execute(text("FLUSH TABLES;"))
            print(f"✅ Tabellen nach Trigger flush erfolgreich.")

    except Exception as e:
        print(f"❌ Fehler beim Flush der Tabellen: {e}")


def view_table():
    if request.method in ['POST', 'GET']:
        selected_table = (
            request.form.get('selected_table')
            if request.method == 'POST'
            else request.args.get('selected_table')
        )

        if selected_table:
            selected_table = selected_table.lower()

            run_trigger_for_table(selected_table)

            page = int(request.args.get('page', 1))
            rows_per_page = 10

            meta = MetaData()
            meta.reflect(bind=mysql_engine)
            table = meta.tables[selected_table]
            rows = []
            total_rows = 0

            with mysql_engine.connect() as conn:
                try:
                    count_query = text(f"SELECT COUNT(*) FROM {selected_table}")
                    total_rows_query = conn.execute(count_query)
                    total_rows = total_rows_query.scalar()

                    offset = (page - 1) * rows_per_page
                    query = table.select().limit(rows_per_page).offset(offset)
                    result = conn.execute(query)

                    if hasattr(result, 'keys'):
                        rows = [dict(zip(result.keys(), row)) for row in result]
                    else:
                        rows = [row._asdict() for row in result]

                    logger.info(f"{len(rows)} rows loaded from {selected_table}.")
                except Exception as exc:
                    logger.error(f"Error processing rows from {selected_table}: {exc}")
                    rows = []

            total_pages = (total_rows + rows_per_page - 1) // rows_per_page

            return render_template(
                'view_table.html',
                table_name=selected_table,
                rows=rows,
                page=page,
                total_pages=total_pages,
                rows_per_page=rows_per_page,
                selected_table=selected_table
            )

    return redirect(url_for('index'))
