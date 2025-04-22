# Datei: api/routes/route_database_stats.py

import pymongo
import logging
from flask import jsonify
from infrastructure.database.helpers.helpers import get_mysql_connection
from infrastructure.config.config import MYSQL_DB_NAME, MONGO_CONFIG_STRING, MONGO_DB_NAME

logger = logging.getLogger(__name__)

def get_database_stats():
    stats = {"MongoDB": {}, "MySQL": {}}
    try:
        conn = get_mysql_connection()
        query = """
            SELECT table_name, table_rows AS total_rows, CREATE_TIME AS last_updated
            FROM information_schema.tables
            WHERE table_schema = %s;
        """
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (MYSQL_DB_NAME,))
        tables = cursor.fetchall()
        for table in tables:
            normalized = {k.lower(): v for k, v in table.items()}
            stats["MySQL"][normalized["table_name"]] = {
                "total_rows": normalized.get("total_rows", "N/A"),
                "last_updated": normalized.get("last_updated", "N/A")
            }
        cursor.close()
        conn.close()
        logger.info("/database-stats: MySQL stats fetched.")
    except Exception as e:
        stats["MySQL"]["error"] = str(e)
        logger.error(f"MySQL stats error: {e}")

    try:
        client = pymongo.MongoClient(MONGO_CONFIG_STRING)
        db = client[MONGO_DB_NAME]
        for name in db.list_collection_names():
            count = db[name].count_documents({})
            last_doc = db[name].find_one(sort=[("_id", -1)])
            stats["MongoDB"][name] = {
                "total_rows": count,
                "last_updated": last_doc["_id"].generation_time.strftime('%Y-%m-%d %H:%M:%S') if last_doc else "N/A"
            }
        logger.info("/database-stats: MongoDB stats fetched.")
    except Exception as e:
        stats["MongoDB"]["error"] = str(e)
        logger.error(f"MongoDB stats error: {e}")

    return jsonify(stats)
