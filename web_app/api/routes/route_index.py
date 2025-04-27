# Datei: api/routes/route_index.py

import logging
from flask import render_template
from infrastructure.database.helpers.helpers import get_tables, get_mysql_connection
from infrastructure.config.config import MYSQL_DB_NAME

logger = logging.getLogger(__name__)

def index():
    tables = get_tables()
    logger.info("Loaded table list for index page.")

    mysql_stats = {}

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        # Hole alle Tabellenamen
        cursor.execute("""
            SELECT table_name, IFNULL(create_time, 'N/A') AS last_updated
            FROM information_schema.tables
            WHERE table_schema = %s;
        """, (MYSQL_DB_NAME,))
        rows = cursor.fetchall()

        # Für jede Tabelle: echten COUNT(*) abfragen
        for row in rows:
            table_name = row.get("table_name")
            if table_name:
                try:
                    # Hole die exakte Anzahl an Zeilen
                    cursor.execute(f"SELECT COUNT(*) AS total_rows FROM `{table_name}`")
                    count_result = cursor.fetchone()
                    total_rows = count_result.get("total_rows", 0)

                    mysql_stats[table_name] = {
                        "total_rows": total_rows,
                        "last_updated": row.get("last_updated", "N/A")
                    }
                except Exception as count_err:
                    logger.error(f"Fehler beim Zählen der Rows in Tabelle {table_name}: {count_err}")
                    mysql_stats[table_name] = {
                        "total_rows": "Error",
                        "last_updated": row.get("last_updated", "N/A")
                    }

        cursor.close()
        conn.close()
        logger.info("MySQL stats loaded successfully.")

    except Exception as e:
        mysql_stats["error"] = str(e)
        logger.error(f"Error loading MySQL stats: {e}")

    stats = {
        "MySQL": mysql_stats,
        "MongoDB": {}
    }

    return render_template('index.html', tables=tables, app_version='0.2.14', stats=stats)
