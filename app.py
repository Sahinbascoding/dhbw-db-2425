import os
import sys
import logging
import atexit
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Basispfade setzen
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WEBAPP_DIR = os.path.join(BASE_DIR, 'web_app')
sys.path.append(WEBAPP_DIR)

# .env laden & Variablen einlesen
load_dotenv()

# Flask App initialisieren
TEMPLATE_DIR = os.path.join(WEBAPP_DIR, 'templates')
STATIC_DIR = os.path.join(WEBAPP_DIR, 'static')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = os.getenv("SECRET_KEY")

# Logging aktivieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# MySQL Konfiguration
from infrastructure.config.config import MYSQL_CONFIG_STRING
mysql_engine = create_engine(MYSQL_CONFIG_STRING)
mysql_session = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

def test_mysql_connection():
    try:
        with mysql_engine.connect() as connection:
            return connection.execute(text("SELECT 1")).scalar() == 1
    except Exception as e:
        logger.error(f"MySQL connection failed: {e}")
        return False

# Routen registrieren
from api.router import register_routes
register_routes(app)

# Datenbank-Reset beim Beenden
from src.tools.reset_db import cleanup_db
atexit.register(cleanup_db)

# App starten
if __name__ == '__main__':
    app.run(debug=False)
