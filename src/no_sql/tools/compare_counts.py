import os
import sys

# Dynamisch Pfad zur web-app hinzufügen
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
WEBAPP_DIR = os.path.join(BASE_DIR, 'web-app')
sys.path.append(WEBAPP_DIR)

from infrastructure.config.config import MYSQL_TABLES, MONGO_CONFIG_STRING, MYSQL_CONFIG_STRING
from sqlalchemy import create_engine, text
import pymongo



def compare_mysql_mongo_counts():
    print("Vergleich der Einträge zwischen MySQL und MongoDB:\n")
    
    # MySQL-Verbindung aufbauen
    mysql_engine = create_engine(MYSQL_CONFIG_STRING)
    mongo_client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    mongo_db = mongo_client["telematik_nosql"]

    with mysql_engine.connect() as conn:
        for table in MYSQL_TABLES:
            # Zähle Zeilen in MySQL
            mysql_count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()

            # Zähle Dokumente in MongoDB
            mongo_count = mongo_db[table].count_documents({})

            # Ausgabe mit Bewertung
            if mysql_count == mongo_count:
                status = "✅ OK"
            else:
                status = "❌ Unterschied!"

            print(f"{table:<25} | MySQL: {mysql_count:<8} | MongoDB: {mongo_count:<8} | {status}")


# Funktion aufrufen
if __name__ == "__main__":
    compare_mysql_mongo_counts()
