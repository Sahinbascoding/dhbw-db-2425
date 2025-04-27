import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
sys.path.append(BASE_DIR)

from sqlalchemy import create_engine, text
import os
import subprocess
from sqlalchemy import MetaData
from sqlalchemy import create_engine, text
from web_app.infrastructure.config.config import MYSQL_CONFIG_STRING,  MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB_NAME

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
    except Exception as e:
        print("Fehler beim Aktivieren von local_infile:", e)

def import_stored_procedures():
    procedures_dir = os.path.join(BASE_DIR, "src", "sql", "procedures")
    if not os.path.exists(procedures_dir):
        print("⚠️ Kein Procedures-Ordner gefunden.")
        return

    for filename in os.listdir(procedures_dir):
        if filename.endswith(".sql"):
            filepath = os.path.join(procedures_dir, filename)
            mysql_command = [
                "mysql",
                "-h", MYSQL_HOST,
                "-u", MYSQL_USER,
                f"-p{MYSQL_PASSWORD}",
                MYSQL_DB_NAME
            ]
            try:
                with open(filepath, "rb") as sql_file:
                    subprocess.run(mysql_command, stdin=sql_file, check=True)
                print(f"✅ Stored Procedure geladen: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Fehler beim Laden der Stored Procedure {filename}: {e}")


def import_sql():
    enable_local_infile()

    try:
        with engine.begin() as connection:
            run_sql_file(os.path.join(BASE_DIR, "src/sql/import/create_shema.sql"))
            run_sql_file(os.path.join(BASE_DIR, "src/sql/import/load_data.sql"))
            run_sql_file(os.path.join(BASE_DIR, "src/sql/import/update_fahrt.sql"))
            run_sql_file(os.path.join(BASE_DIR, "src/sql/import/data_cleanup.sql"))

        import_stored_procedures()
        return True
    except Exception as e:
        print("❌ SQL-Import fehlgeschlagen:", e)
        return False
