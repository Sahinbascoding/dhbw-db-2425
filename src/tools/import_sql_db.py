import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
sys.path.append(BASE_DIR)

from sqlalchemy import create_engine, text
from web_app.infrastructure.config.config import MYSQL_CONFIG_STRING

engine = create_engine(
    MYSQL_CONFIG_STRING,
    connect_args={"local_infile": 1}
)

def run_sql_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        sql_commands = file.read()

    # Absoluten Pfad zu data/ holen (mit richtigen Slashes)
    data_dir = os.path.abspath(os.path.join(BASE_DIR, "data"))
    data_dir = data_dir.replace("\\", "/")  # Sicherstellen, dass Windows Slashes korrekt sind!

    # Ersetze den Platzhalter im SQL
    sql_commands = sql_commands.replace(
        "LOAD DATA LOCAL INFILE 'data/",
        f"LOAD DATA LOCAL INFILE '{data_dir}/"
    )

    with engine.connect() as connection:
        for statement in sql_commands.split(";"):
            stmt = statement.strip()
            if stmt:
                connection.execute(text(stmt))


def import_sql():
    print("📦 Starte SQL-Import...")
    try:
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/create_shema.sql"))
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/load_data.sql"))
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/update_fahrt.sql"))
        run_sql_file(os.path.join(BASE_DIR, "src/sql/import/data_cleanup.sql"))
        print("✅ SQL-Import erfolgreich abgeschlossen.")
        return True
    except Exception as e:
        print(f"❌ Fehler beim SQL-Import: {e}")
        return False
