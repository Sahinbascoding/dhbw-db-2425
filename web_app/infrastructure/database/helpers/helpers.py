import pymongo
import mysql.connector
from sqlalchemy import MetaData
import os
from datetime import datetime, date
from infrastructure.config.config import (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME, MONGO_DB_NAME,
                                          ALLOWED_TABLES, ALLOWED_EXTENSIONS, MONGO_CONFIG_STRING)
from src.no_sql.convert_to_mongo import convert_single_table, convert_embedded
from src.no_sql.utils import fix_dates  # <- ausgelagerte Hilfsfunktion


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def get_tables():
    """
    Reads all tables from the relational database using automatic reflection.
    """
    from app import mysql_engine  # Import here to avoid circular dependency
    meta = MetaData()
    meta.reflect(bind=mysql_engine)
    return meta.tables.keys()


def get_mongo_client():
    """
    Returns a new MongoDB client instance.
    """
    return pymongo.MongoClient(MONGO_CONFIG_STRING)


def insert_message_to_mysql(message, duration):
    """
    Inserts a success or error message into the 'success_logs' table in MySQL.
    """
    try:

        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO success_logs (message, duration, timestamp)
            VALUES (%s, %s, NOW());
        """

        cursor.execute(query, (message, duration))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error writing success message to MySQL: {err}")


def allowed_file(filename):
    """
    Checks whether the provided filename has an allowed extension (JSON).
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_mysql_connection():
    """
    Returns a new MySQL database connection.
    Use this function to avoid repeated connection setups.
    """
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME
    )



def get_db(table_name=None):
    """
    Returns a database connection based on the table name:
    - MySQL for relational tables
    - MongoDB for NoSQL collections
    """
    if table_name in ALLOWED_TABLES:
        return get_mysql_connection()
    else:
        # Return MongoDB collection for NoSQL collections
        mongo_client = get_mongo_client()
        db = mongo_client[os.getenv("MONGO_DB_NAME", "production")]
        return db[table_name]


def convert_to_mongodb(selected_tables, embed=True):
    """
    Converts specified tables from MySQL to MongoDB. If 'embed' is True, it embeds
    related data into a single 'embedded' collection; otherwise, each table is
    converted to its own MongoDB collection.
    """
    from app import mysql_engine, mysql_session

    client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    db = client[MONGO_DB_NAME]

    session = mysql_session()
    meta = MetaData()
    meta.reflect(bind=mysql_engine)

    total_inserted = 0

    if embed:
        total_inserted = convert_embedded(selected_tables, mysql_engine, db)
    else:
        for table in selected_tables:
            total_inserted += convert_single_table(table, mysql_engine, db)

    session.close()
    print("Conversion completed.")
    return total_inserted

def log_conversion_to_mysql(source_table, target_collection, status, duration):
    """
    Inserts a log entry into the conversion_log table after a table has been converted.
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO conversion_log (source_table, target_collection, status, duration_seconds, timestamp)
            VALUES (%s, %s, %s, %s, NOW());
        """
        cursor.execute(query, (source_table, target_collection, status, duration))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error writing conversion log to MySQL: {err}")

