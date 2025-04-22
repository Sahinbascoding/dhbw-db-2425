import os
import sys
from sqlalchemy import create_engine, text
import pymongo

# Dynamisch Pfad zur web_app hinzufügen
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
WEBAPP_DIR = os.path.join(BASE_DIR, 'web_app')
sys.path.append(WEBAPP_DIR)

from infrastructure.config.config import (
    MYSQL_CONFIG_STRING,
    MYSQL_DB_NAME,
    MONGO_CONFIG_STRING,
    MONGO_DB_NAME
)


def reset_mysql():
    """MySQL-Datenbank löschen und neu erstellen."""
    try:
        engine = create_engine(MYSQL_CONFIG_STRING)
        with engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS {MYSQL_DB_NAME}"))
            conn.execute(text(f"CREATE DATABASE {MYSQL_DB_NAME}"))
        print(f"[MySQL] Datenbank '{MYSQL_DB_NAME}' wurde neu erstellt.")
    except Exception as e:
        print(f"[MySQL] Fehler beim Zurücksetzen: {e}")


def reset_mongo():
    """MongoDB-Datenbank löschen."""
    try:
        client = pymongo.MongoClient(MONGO_CONFIG_STRING)
        client.drop_database(MONGO_DB_NAME)
        print(f"[MongoDB] Datenbank '{MONGO_DB_NAME}' wurde gelöscht.")
    except Exception as e:
        print(f"[MongoDB] Fehler beim Zurücksetzen: {e}")


def cleanup_db():
    """Führt beide Resets aus."""
    print("📦 Starte Zurücksetzen der Datenbanken...")
    reset_mysql()
    reset_mongo()
    print("✅ Datenbanken wurden zurückgesetzt.")


# Optionaler direkter Aufruf
if __name__ == "__main__":
    cleanup_db()
