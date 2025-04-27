import os
import sys
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
sys.path.append(BASE_DIR)

from web_app.infrastructure.config.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB_NAME
from sqlalchemy import create_engine, text
from web_app.infrastructure.config.config import MYSQL_CONFIG_STRING

mysql_engine = create_engine(MYSQL_CONFIG_STRING)

def run_trigger_for_table(table_name):
    trigger_dir = os.path.join(BASE_DIR, "src/sql/triggers")
    trigger_filename = f"{table_name}_trigger.sql"
    trigger_filepath = os.path.join(trigger_dir, trigger_filename)

    if not os.path.exists(trigger_filepath):
        print(f"⚠️ Kein Trigger-SQL-File für {table_name} gefunden.")
        return

    mysql_command = [
        "mysql",
        "-h", MYSQL_HOST,
        "-u", MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        MYSQL_DB_NAME
    ]

    try:
        with open(trigger_filepath, "rb") as sql_file:
            subprocess.run(mysql_command, stdin=sql_file, check=True)
        print(f"✅ Trigger für Tabelle '{table_name}' erfolgreich ausgeführt.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Trigger '{table_name}': {e}")
        return

    # Tabellen flushen
    try:
        with mysql_engine.connect() as connection:
            connection.execute(text("FLUSH TABLES;"))
        print("✅ Tabellen nach Trigger flush erfolgreich.")
    except Exception as e:
        print(f"❌ Fehler beim Flush: {e}")

def activate_triggers():
    trigger_tables = [
        "beschleunigung", "conversion_log", "diagnose", "fahrer_fahrzeug",
        "fahrer", "fahrt_fahrer", "fahrt", "fahrzeugparameter",
        "fahrzeug", "geraet_installation", "geraet", "wartung"
    ]

    for table in trigger_tables:
        run_trigger_for_table(table)
