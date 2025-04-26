import os
import sys
from sqlalchemy import create_engine, text
from infrastructure.config.config import MYSQL_CONFIG_STRING, MYSQL_DB_NAME

# Base-Pfad ermitteln
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Engine
engine = create_engine(
    MYSQL_CONFIG_STRING,
    connect_args={"local_infile": 1}
)


def run_sql_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        sql_commands = file.read()
    with engine.connect() as connection:
        for statement in sql_commands.split(";"):
            stmt = statement.strip()
            if stmt:
                connection.execute(text(stmt))
def enable_local_infile():
    try:
        with engine.connect() as connection:
            connection.execute(text("SET GLOBAL local_infile = 1;"))
            print("✅ local_infile auf Server aktiviert.")
    except Exception as e:
        print("❌ Fehler beim Aktivieren von local_infile:", e)


def import_sql():
    print("📦 Starte SQL-Import...")

    enable_local_infile() 

    try:
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/create_shema.sql"))
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/load_data.sql"))
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/update_fahrt.sql"))
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/data_cleanup.sql"))
        
        print("✅ SQL-Import abgeschlossen.")
        return True
    except Exception as e:
        print("❌ SQL-Import fehlgeschlagen:", e)
        return False
