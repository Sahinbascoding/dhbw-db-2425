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
        query = """
            SELECT
                table_name,
                table_rows AS total_rows,
                CREATE_TIME AS last_updated
            FROM information_schema.tables
            WHERE table_schema = %s;
        """
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (MYSQL_DB_NAME,))
        rows = cursor.fetchall()
        for row in rows:
            mysql_stats[row["table_name"]] = {
                "total_rows": row["total_rows"] if row["total_rows"] is not None else "N/A",
                "last_updated": row["last_updated"] if row["last_updated"] else None
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
