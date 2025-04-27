# Datei: api/routes/route_database_stats.py

import pymongo
import logging
from flask import jsonify
from infrastructure.database.helpers.helpers import get_mysql_connection
from infrastructure.config.config import MYSQL_DB_NAME, MONGO_CONFIG_STRING, MONGO_DB_NAME, ALLOWED_TABLES

logger = logging.getLogger(__name__)

def get_database_stats():
    stats = {"MongoDB": {}, "MySQL": {}}
    
    # --- MySQL exakte Statistiken ---
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        # Tabellenamen & Erstellungszeit holen
        cursor.execute("""
            SELECT TABLE_NAME, IFNULL(CREATE_TIME, NOW()) AS last_updated
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_type = 'BASE TABLE';
        """, (MYSQL_DB_NAME,))
        tables = cursor.fetchall()

        for table in tables:
            table_name = table.get('TABLE_NAME')
            if not table_name:
                continue

            try:
                # Echten Row-Count für jede Tabelle holen
                cursor.execute(f"SELECT COUNT(*) AS total_rows FROM `{table_name}`")
                count_result = cursor.fetchone()
                total_rows = count_result.get("total_rows", 0)

                stats["MySQL"][table_name.lower()] = {
                    "total_rows": total_rows,
                    "last_updated": table.get('last_updated') or "-"
                }
            except Exception as count_err:
                logger.error(f"MySQL COUNT(*) Fehler in {table_name}: {count_err}")
                stats["MySQL"][table_name.lower()] = {
                    "total_rows": "Error",
                    "last_updated": table.get('last_updated') or "-"
                }

        cursor.close()
        conn.close()
        logger.info("/database-stats: MySQL stats fetched.")

    except Exception as e:
        stats["MySQL"]["error"] = str(e)
        logger.error(f"MySQL stats error: {e}")

    # --- MongoDB Statistiken ---
    try:
        client = pymongo.MongoClient(MONGO_CONFIG_STRING)
        db = client[MONGO_DB_NAME]


        existing_collections = db.list_collection_names()

        for name in ALLOWED_TABLES:
            if name in existing_collections:
                collection = db[name]
                count = collection.count_documents({})
                last_doc = collection.find_one(sort=[("_id", -1)])
                stats["MongoDB"][name] = {
                    "total_rows": count,
                    "last_updated": last_doc["_id"].generation_time.strftime('%Y-%m-%d %H:%M:%S') if last_doc else "-"
                }

        logger.info("/database-stats: MongoDB stats fetched.")
    except Exception as e:
        stats["MongoDB"]["error"] = str(e)
        logger.error(f"MongoDB stats error: {e}")

    return jsonify(stats)
