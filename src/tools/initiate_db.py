import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
sys.path.append(BASE_DIR)

from src.tools.enable_local_infile import enable_local_infile
from src.tools.import_sql_db1 import import_sql
from src.tools.activate_triggers import activate_triggers
from src.tools.activate_procedures import activate_stored_procedures

def initiate_db():
    enable_local_infile()
    success = import_sql()
    if not success:
        print("⚠️ SQL-Import fehlgeschlagen, fahre trotzdem fort...")
    activate_triggers()
    activate_stored_procedures()
    print("✅ Datenbank vollständig initialisiert!")
