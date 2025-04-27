import os
import sys
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
sys.path.append(BASE_DIR)

from web_app.infrastructure.config.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB_NAME

def activate_stored_procedures():
    procedures_dir = os.path.join(BASE_DIR, "src/sql/procedures")
    if not os.path.exists(procedures_dir):
        print("⚠️ Kein Procedures-Ordner gefunden.")
        return

    mysql_command = [
        "mysql",
        "-h", MYSQL_HOST,
        "-u", MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        MYSQL_DB_NAME
    ]

    for filename in os.listdir(procedures_dir):
        if filename.endswith(".sql"):
            filepath = os.path.join(procedures_dir, filename)
            try:
                with open(filepath, "rb") as sql_file:
                    subprocess.run(mysql_command, stdin=sql_file, check=True)
                print(f"✅ Stored Procedure geladen: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Fehler beim Laden der Stored Procedure {filename}: {e}")
