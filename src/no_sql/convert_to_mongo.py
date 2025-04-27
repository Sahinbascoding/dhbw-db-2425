from sqlalchemy import MetaData, Table, select
from src.no_sql.utils import fix_dates
from infrastructure.config.config import MYSQL_TABLES

def convert_single_table(table_name, mysql_engine, db):
    """
    Converts a single MySQL table into a MongoDB collection (1:1 Abbildung).
    """
    meta = MetaData()
    meta.reflect(bind=mysql_engine)
    table = meta.tables[table_name]

    with mysql_engine.connect() as conn:
        result = conn.execute(select(table))
        rows = [fix_dates(dict(row._mapping)) for row in result]

    if rows:
        db[table_name].delete_many({})  # optional: vorher leeren
        db[table_name].insert_many(rows)
        print(f"[MongoDB] Inserted {len(rows)} documents into '{table_name}'")
        return len(rows)
    return 0

def convert_embedded(tables, mysql_engine, db):
    """
    Converts related MySQL tables into a single embedded MongoDB collection.
    Beispiel: fahrer mit eingebetteten fahrten
    """
    normalized_tables = set([t.lower() for t in tables])

    if not {"fahrer", "fahrt", "fahrt_fahrer"}.issubset(normalized_tables):
        print("[MongoDB] Required tables for embedding (fahrer, fahrt, fahrt_fahrer) not provided.")
        return 0

    meta = MetaData()
    meta.reflect(bind=mysql_engine)

    fahrer = meta.tables["fahrer"]
    fahrt = meta.tables["fahrt"]
    fahrt_fahrer = meta.tables["fahrt_fahrer"]

    with mysql_engine.connect() as conn:
        # Hole alle fahrer
        fahrer_result = conn.execute(select(fahrer))
        fahrer_docs = []

        for f in fahrer_result:
            f_dict = fix_dates(dict(f._mapping))

            # fahrten des fahrers finden
            join_stmt = (
                select(fahrt)
                .select_from(fahrt.join(fahrt_fahrer, fahrt.c.fahrtid == fahrt_fahrer.c.fahrtid))
                .where(fahrt_fahrer.c.fahrerid == f.fahrerid)
            )

            fahrten_result = conn.execute(join_stmt)
            fahrten = [fix_dates(dict(row._mapping)) for row in fahrten_result]

            f_dict["fahrten"] = fahrten
            fahrer_docs.append(f_dict)

    if fahrer_docs:
        db["fahrer_mit_fahrten"].delete_many({})
        db["fahrer_mit_fahrten"].insert_many(fahrer_docs)
        print(f"[MongoDB] Inserted {len(fahrer_docs)} embedded documents into 'fahrer_mit_fahrten'")
        return len(fahrer_docs)
    return 0

def convert_to_mongodb(selected_tables, embed=True):
    """
    Converts specified tables from MySQL to MongoDB. 
    - embed=True: embeds related data
    - embed=False: 1:1 conversion per table
    """
    from app import mysql_engine, mysql_session
    import pymongo
    from infrastructure.config.config import MONGO_CONFIG_STRING, MONGO_DB_NAME

    client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    db = client[MONGO_DB_NAME]

    session = mysql_session()

    # Filter nur gültige SQL-Tabellen
    valid_tables = [t for t in selected_tables if t in MYSQL_TABLES]
    skipped = [t for t in selected_tables if t not in MYSQL_TABLES]

    if skipped:
        print(f"[MongoDB] Skipping unsupported tables: {skipped}")

    total_inserted = 0

    normalized_tables = set([t.lower() for t in valid_tables])

    # 1. Embedded Collection nur erzeugen wenn ALLE 3 Tabellen vorhanden
    if {"fahrer", "fahrt", "fahrt_fahrer"}.issubset(normalized_tables):
        total_inserted += convert_embedded(["fahrer", "fahrt", "fahrt_fahrer"], mysql_engine, db)
        
        # Nach Embedding: Diese 3 Tabellen aus der normalen Liste rausnehmen
        valid_tables = [t for t in valid_tables if t.lower() not in {"fahrer", "fahrt", "fahrt_fahrer"}]

    # 2. Alle übrigen Tabellen normal konvertieren
    for table in valid_tables:
        total_inserted += convert_single_table(table, mysql_engine, db)

    session.close()
    print("Conversion completed.")
    return total_inserted


