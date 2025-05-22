from sqlalchemy import MetaData, select
from src.no_sql.utils import fix_dates
from infrastructure.config.config import MONGO_CONFIG_STRING, MONGO_DB_NAME, MYSQL_TABLES
from app import mysql_engine, mysql_session
import pymongo
from collections import defaultdict


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
        db[table_name].delete_many({})
        db[table_name].insert_many(rows)
        print(f"[MongoDB] Inserted {len(rows)} documents into '{table_name}'")
        return len(rows)
    return 0


def convert_embedded(tables, mysql_engine, db):
    """
    Converts related MySQL tables into embedded MongoDB documents centered around 'fahrt'.
    """
    meta = MetaData()
    meta.reflect(bind=mysql_engine)
    normalized = set(t.lower() for t in tables)

    if "fahrt" not in normalized:
        print("[MongoDB] ❌ Tabelle 'fahrt' muss für Embedding enthalten sein.")
        return 0

    fahrt = meta.tables["fahrt"]
    fahrzeug = meta.tables.get("fahrzeug")
    geraet = meta.tables.get("geraet")
    fahrer = meta.tables.get("fahrer")
    fahrt_fahrer = meta.tables.get("fahrt_fahrer")
    fahrzeugparameter = meta.tables.get("fahrzeugparameter")
    diagnose = meta.tables.get("diagnose")
    beschleunigung = meta.tables.get("beschleunigung")
    wartung = meta.tables.get("wartung")
    geraet_installation = meta.tables.get("geraet_installation")

    with mysql_engine.connect() as conn:
        # Hauptfahrten laden
        fahrt_rows = [fix_dates(dict(r._mapping)) for r in conn.execute(select(fahrt))]

        # Hilfsfunktionen zur Vorverarbeitung
        def load_map(table, key):
            return {
                row._mapping[key]: fix_dates(dict(row._mapping))
                for row in conn.execute(select(table))
                if key in row._mapping
            }

        def load_grouped(table, key):
            grouped = defaultdict(list)
            for row in conn.execute(select(table)):
                r = fix_dates(dict(row._mapping))
                grouped[r[key]].append(r)
            return grouped

        # Daten vorbereiten (nur wenn Tabelle ausgewählt ist)
        fahrzeug_map = load_map(fahrzeug, "fahrzeugid") if "fahrzeug" in normalized else {}
        geraet_map = load_map(geraet, "geraetid") if "geraet" in normalized else {}
        fahrzeugparameter_map = load_grouped(fahrzeugparameter, "fahrtid") if "fahrzeugparameter" in normalized else {}
        diagnose_map = load_grouped(diagnose, "fahrtid") if "diagnose" in normalized else {}
        beschleunigung_map = load_grouped(beschleunigung, "fahrtid") if "beschleunigung" in normalized else {}
        wartung_map = load_grouped(wartung, "fahrzeugid") if "wartung" in normalized else {}
        installation_map = load_grouped(geraet_installation, "fahrzeugid") if "geraet_installation" in normalized else {}

        fahrer_map = defaultdict(list)
        if "fahrer" in normalized and "fahrt_fahrer" in normalized:
            join_stmt = (
                select(fahrt_fahrer.c.fahrtid, fahrer)
                .select_from(fahrer.join(fahrt_fahrer, fahrer.c.fahrerid == fahrt_fahrer.c.fahrerid))
            )
            for row in conn.execute(join_stmt):
                fahrtid = row._mapping["fahrtid"]
                fahrer_map[fahrtid].append(fix_dates(dict(row._mapping)))

    # Dokumente zusammenstellen
    fahrt_docs = []
    for f in fahrt_rows:
        fid = f["fahrtid"]
        vid = f.get("fahrzeugid")
        gid = f.get("geraetid")

        if "fahrzeug" in normalized:
            f["fahrzeug"] = fahrzeug_map.get(vid)
        if "geraet" in normalized:
            f["geraet"] = geraet_map.get(gid)
        if "fahrer" in normalized and "fahrt_fahrer" in normalized:
            f["fahrer"] = fahrer_map.get(fid)
        if "fahrzeugparameter" in normalized:
            f["fahrzeugparameter"] = fahrzeugparameter_map.get(fid)
        if "diagnose" in normalized:
            f["diagnose"] = diagnose_map.get(fid)
        if "beschleunigung" in normalized:
            f["beschleunigung"] = beschleunigung_map.get(fid)
        if "wartung" in normalized:
            f["wartung"] = wartung_map.get(vid)
        if "geraet_installation" in normalized:
            f["geraet_installation"] = installation_map.get(vid)

        fahrt_docs.append(f)

    if fahrt_docs:
        db["fahrt_embedded"].delete_many({})
        db["fahrt_embedded"].insert_many(fahrt_docs)
        print(f"[MongoDB] ✅ {len(fahrt_docs)} embedded documents in 'fahrt_embedded'")
        return len(fahrt_docs)

    print("[MongoDB] ⚠️ Keine Fahrten zum Einbetten gefunden.")
    return 0


def convert_to_mongodb(selected_tables, embed=True):
    """
    Main entry point: converts selected MySQL tables to MongoDB.
    - embed=False: creates 1:1 collections.
    - embed=True: creates a single embedded 'fahrt_embedded' collection.
    """
    client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    db = client[MONGO_DB_NAME]
    session = mysql_session()

    sql_tables = [t for t in selected_tables if t in MYSQL_TABLES]
    skipped = [t for t in selected_tables if t not in MYSQL_TABLES]

    if skipped:
        print(f"[MongoDB] ⚠️ Überspringe ungültige Tabellen: {skipped}")

    total_inserted = 0

    if not embed:
        for table in sql_tables:
            total_inserted += convert_single_table(table, mysql_engine, db)
        session.close()
        print("✅ Flat-Konvertierung abgeschlossen.")
        return total_inserted

    # Prüfung auf notwendige Tabellen für Embedding
    normalized = set(t.lower() for t in selected_tables)
    fahrt_relevante = {
        "fahrer", "fahrt", "fahrt_fahrer", "fahrzeug", "geraet",
        "fahrzeugparameter", "diagnose", "beschleunigung",
        "wartung", "geraet_installation"
    }

    selected_relevant = normalized.intersection(fahrt_relevante)

    if "fahrt" not in selected_relevant:
        print("❌ Für eingebettete Konvertierung muss 'fahrt' ausgewählt sein.")
        return 0

    if len(selected_relevant) < 2:
        print("❌ Es müssen mindestens 'fahrt' und eine weitere passende Tabelle ausgewählt werden.")
        return 0

    total_inserted += convert_embedded(selected_tables, mysql_engine, db)
    session.close()
    print("✅ Eingebettete Konvertierung abgeschlossen.")
    return total_inserted
