# Datei: src/nosql/insert_json_to_mongo.py

import os
import json
import pymongo
from infrastructure.config.config import MONGO_CONFIG_STRING, MONGO_DB_NAME

def insert_json_to_mongo(json_path, collection_name):
    """
    Liest eine JSON-Datei ein und fügt sie in eine angegebene MongoDB-Collection ein.
    """

    client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    db = client[MONGO_DB_NAME]

    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"Datei {json_path} existiert nicht!")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict):
        db[collection_name].insert_one(data)
        print(f"✅ 1 Dokument erfolgreich in {collection_name} eingefügt.")
    elif isinstance(data, list):
        if data:
            db[collection_name].insert_many(data)
            print(f"✅ {len(data)} Dokumente erfolgreich in {collection_name} eingefügt.")
        else:
            print("⚠️ JSON-Datei enthält ein leeres Array. Keine Dokumente eingefügt.")
    else:
        raise ValueError("❌ Ungültiges JSON-Format. Muss Objekt oder Array von Objekten sein.")

if __name__ == "__main__":
    # Beispiel-Aufruf:
    try:
        insert_json_to_mongo("data/unfall.json", "unfall")
    except Exception as e:
        print(f"❌ Fehler beim Einfügen: {e}")
