# Datei: api/routes/route_add_data.py

import json
import logging
import pymongo
from flask import render_template, request
from infrastructure.config.config import MONGO_CONFIG_STRING, MONGO_DB_NAME, ALLOWED_TABLES
from infrastructure.database.helpers.helpers import allowed_file

logger = logging.getLogger(__name__)

def add_data():
    client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    db = client[MONGO_DB_NAME]
    success_message = None
    error_message = None

    if request.method == 'POST':
        collection_choice = request.form.get('collection_choice')
        logger.info("Processing data import...")

        if collection_choice == 'existing':
            selected_table = request.form.get('table_name')
            if selected_table not in ALLOWED_TABLES:
                error_message = "Invalid table selected."
                return render_template('add_data.html', tables=ALLOWED_TABLES, success_message=success_message, error_message=error_message)
            target_collection = selected_table
        else:
            new_collection_name = request.form.get('new_collection_name')
            if not new_collection_name or new_collection_name.strip() == "":
                error_message = "Please provide a valid name for the new collection."
                return render_template('add_data.html', tables=ALLOWED_TABLES, success_message=success_message, error_message=error_message)
            target_collection = new_collection_name.strip()

        if 'json_file' not in request.files:
            error_message = "No file uploaded."
        else:
            file = request.files['json_file']
            if file.filename == '':
                error_message = "No file selected."
            elif file and allowed_file(file.filename):
                file_content = file.read().decode('utf-8')
                try:
                    data = json.loads(file_content)
                    if isinstance(data, dict):
                        db[target_collection].insert_one(data)
                        success_message = "Successfully added one document!"
                    elif isinstance(data, list):
                        if data:
                            db[target_collection].insert_many(data)
                            success_message = f"{len(data)} documents successfully added!"
                        else:
                            error_message = "The JSON file contains an empty array."
                    else:
                        error_message = "The JSON file must contain either an object or an array of objects."
                    logger.info(success_message or error_message)
                except json.JSONDecodeError as exc:
                    error_message = f"Invalid JSON format: {exc}"
                    logger.error(error_message)
            else:
                error_message = "Invalid file type. Please upload a .json file."

    return render_template('add_data.html', tables=ALLOWED_TABLES, success_message=success_message, error_message=error_message)
