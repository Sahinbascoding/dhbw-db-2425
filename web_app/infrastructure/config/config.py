import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_PORT = os.getenv("MONGO_PORT")

MYSQL_CONFIG_STRING = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB_NAME}?local_infile=1"
MONGO_CONFIG_STRING = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

ALLOWED_EXTENSIONS = {'json'}

# ALLOWED_TABLES = [
#     'fahrzeug', 'fahrer', 'fahrt', 'fahrt_fahrer', 'fahrzeugparameter',
#     'beschleunigung', 'geraet', 'geraet_installation',
#     'diagnose', 'wartung', 'unfall'
# ]
MYSQL_TABLES = [
    'fahrzeug', 'fahrer', 'fahrer_fahrzeug', 'geraet', 'fahrt',
    'fahrt_fahrer', 'fahrzeugparameter', 'beschleunigung',
    'diagnose', 'wartung', 'geraet_installation'
]

MONGO_JSON_COLLECTIONS = ['unfall']

ALLOWED_TABLES = MYSQL_TABLES + MONGO_JSON_COLLECTIONS



