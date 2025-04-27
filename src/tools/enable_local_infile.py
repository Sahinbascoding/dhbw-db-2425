import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
sys.path.append(BASE_DIR)

from web_app.infrastructure.config.config import MYSQL_CONFIG_STRING
from sqlalchemy import create_engine, text

engine = create_engine(
    MYSQL_CONFIG_STRING,
    connect_args={"local_infile": 1}
)

def enable_local_infile():
    try:
        with engine.connect() as connection:
            connection.execute(text("SET GLOBAL local_infile = 1;"))
        print("✅ local_infile erfolgreich aktiviert.")
    except Exception as e:
        print(f"❌ Fehler beim Aktivieren von local_infile: {e}")
