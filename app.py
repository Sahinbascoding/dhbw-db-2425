import os
import sys
import logging
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------------------- #
# Dynamisch den absoluten Pfad zur web-app setzen
# ----------------------------------------------------------------------------- #
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WEBAPP_DIR = os.path.join(BASE_DIR, 'web-app')

# web-app zur sys.path hinzufügen für Imports
sys.path.append(WEBAPP_DIR)

# ----------------------------------------------------------------------------- #
# Imports aus dem Web-App-Ordner
# ----------------------------------------------------------------------------- #
from infrastructure.config.config import MYSQL_CONFIG_STRING

# ----------------------------------------------------------------------------- #
# Load Environment Variables
# ----------------------------------------------------------------------------- #
load_dotenv()

# ----------------------------------------------------------------------------- #
# Flask Application Setup
# ----------------------------------------------------------------------------- #
TEMPLATE_DIR = os.path.join(WEBAPP_DIR, 'templates')
STATIC_DIR = os.path.join(WEBAPP_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = os.getenv("SECRET_KEY")

# ----------------------------------------------------------------------------- #
# Logging Setup
# ----------------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------- #
# MySQL Setup
# ----------------------------------------------------------------------------- #
mysql_engine = create_engine(MYSQL_CONFIG_STRING)
mysql_session = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

def test_mysql_connection():
    try:
        with mysql_engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            return result == 1
    except Exception as e:
        logger.error(f"MySQL connection failed: {e}")
        return False

# ----------------------------------------------------------------------------- #
# Register Routes
# ----------------------------------------------------------------------------- #
from api.routes.route import register_routes
register_routes(app)

# ----------------------------------------------------------------------------- #
# Main Entrypoint
# ----------------------------------------------------------------------------- #
if __name__ == '__main__':
    app.run(debug=False)
