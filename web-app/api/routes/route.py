from datetime import datetime
import json
import pymongo
import logging
from infrastructure.database.helpers.helpers import (allowed_file, get_tables, convert_to_mongodb,
                                                     insert_message_to_mysql, get_db)
from infrastructure.config.config import MONGO_CONFIG_STRING, MONGO_DB_NAME, ALLOWED_TABLES, MYSQL_TABLES
from sqlalchemy import MetaData, text
from flask import flash
from infrastructure.database.helpers.helpers import get_mysql_connection
from flask import render_template, request, redirect, url_for, jsonify

logger = logging.getLogger(__name__)


def register_routes(app):
    """Registers all Flask routes inside app.py."""

    @app.route('/')
    def index():
        tables = get_tables()
        logger.info("Loaded table list for index page.")

        mysql_stats = {}
        try:
            conn = get_mysql_connection()
            query = """
                SELECT
                    table_name,
                    table_rows AS total_rows,
                    CREATE_TIME AS last_updated
                FROM information_schema.tables
                WHERE table_schema = %s;
            """
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, ("telematik",))
            rows = cursor.fetchall()
            for row in rows:
                mysql_stats[row["table_name"]] = {
                    "total_rows": row["total_rows"] if row["total_rows"] is not None else "N/A",
                    "last_updated": row["last_updated"] if row["last_updated"] else None
                }
            cursor.close()
            conn.close()
            logger.info("MySQL stats loaded successfully.")
        except Exception as e:
            mysql_stats["error"] = str(e)
            logger.error(f"Error loading MySQL stats: {e}")

        stats = {
            "MySQL": mysql_stats,
            "MongoDB": {}
        }

        return render_template(
            'index.html',
            tables=tables,
            app_version='0.2.14',
            stats=stats
        )

    @app.route('/add-data', methods=['GET', 'POST'])
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

    @app.route('/reports', methods=['GET', 'POST'])
    def reports():
        conn = get_mysql_connection()
        available_reports = {
            "fahrten_fahrer": "Anzahl der Fahrten pro Fahrer"
        }

        if request.method == 'POST':
            selected_report = request.form.get('report_type')
            return redirect(url_for('reports', report_type=selected_report))
        else:
            selected_report = request.args.get('report_type')
            page = request.args.get('page', 1, type=int)

        report_data = []
        cursor = conn.cursor()

        if selected_report == "fahrten_fahrer":
            query = """
                SELECT f.fahrerid, f.vorname, f.nachname, COUNT(ff.fahrtid) AS anzahl_fahrten
                FROM fahrer f
                JOIN fahrt_fahrer ff ON f.fahrerid = ff.fahrerid
                GROUP BY f.fahrerid, f.vorname, f.nachname;
            """
            cursor.execute(query)
            report_data = cursor.fetchall()
            report_data = [
                {"fahrerID": row[0], "vorname": row[1], "nachname": row[2], "anzahl_fahrten": row[3]}
                for row in report_data]
            logger.info("Report 'fahrten_fahrer' loaded successfully.")

        cursor.close()
        conn.close()

        items_per_page = 10
        total_items = len(report_data)
        total_pages = (total_items + items_per_page - 1) // items_per_page

        start = (page - 1) * items_per_page
        end = start + items_per_page
        page_data = report_data[start:end]

        return render_template('reports.html', available_reports=available_reports, report_data=page_data, selected_report=selected_report, page=page, total_pages=total_pages)

    @app.route('/database-stats', methods=['GET'])
    def get_database_stats():
        stats = {"MongoDB": {}, "MySQL": {}}
        try:
            conn = get_mysql_connection()
            query = """
                SELECT table_name, table_rows AS total_rows, CREATE_TIME AS last_updated
                FROM information_schema.tables
                WHERE table_schema = %s;
            """
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, ("telematik",))
            tables = cursor.fetchall()
            for table in tables:
                normalized = {k.lower(): v for k, v in table.items()}
                stats["MySQL"][normalized["table_name"]] = {
                    "total_rows": normalized.get("total_rows", "N/A"),
                    "last_updated": normalized.get("last_updated", "N/A")
                }
            cursor.close()
            conn.close()
            logger.info("/database-stats: MySQL stats fetched.")
        except Exception as e:
            stats["MySQL"]["error"] = str(e)
            logger.error(f"MySQL stats error: {e}")

        try:
            client = pymongo.MongoClient(MONGO_CONFIG_STRING)
            db = client[MONGO_DB_NAME]
            for name in db.list_collection_names():
                count = db[name].count_documents({})
                last_doc = db[name].find_one(sort=[("_id", -1)])
                stats["MongoDB"][name] = {
                    "total_rows": count,
                    "last_updated": last_doc["_id"].generation_time.strftime('%Y-%m-%d %H:%M:%S') if last_doc else "N/A"
                }
            logger.info("/database-stats: MongoDB stats fetched.")
        except Exception as e:
            stats["MongoDB"]["error"] = str(e)
            logger.error(f"MongoDB stats error: {e}")

        return jsonify(stats)

    @app.route('/view-table', methods=['GET', 'POST'])
    def view_table():
        from app import mysql_engine
        if request.method in ['POST', 'GET']:
            selected_table = (
                request.form.get('selected_table')
                if request.method == 'POST'
                else request.args.get('selected_table')
            )
            page = int(request.args.get('page', 1))
            rows_per_page = 10

            if selected_table:
                meta = MetaData()
                meta.reflect(bind=mysql_engine)
                table = meta.tables[selected_table]
                rows = []
                total_rows = 0

                with mysql_engine.connect() as conn:
                    try:
                        count_query = text(f"SELECT COUNT(*) FROM {selected_table}")
                        total_rows_query = conn.execute(count_query)
                        total_rows = total_rows_query.scalar()

                        offset = (page - 1) * rows_per_page
                        query = table.select().limit(rows_per_page).offset(offset)
                        result = conn.execute(query)

                        if hasattr(result, 'keys'):
                            rows = [dict(zip(result.keys(), row)) for row in result]
                        else:
                            rows = [row._asdict() for row in result]
                        logger.info(f"{len(rows)} rows loaded from {selected_table}.")
                    except Exception as exc:
                        logger.error(f"Error processing rows from {selected_table}: {exc}")
                        rows = []

                total_pages = (total_rows + rows_per_page - 1) // rows_per_page

                return render_template('view_table.html', table_name=selected_table, rows=rows, page=page, total_pages=total_pages, rows_per_page=rows_per_page, selected_table=selected_table)

        return redirect(url_for('index'))

    @app.route('/convert', methods=['GET', 'POST'])
    def convert():
        if request.method == 'POST':
            selected_tables = request.form.getlist('tables')
            convert_all = request.form.get('convert_all')
            embed = request.form.get('embed')

            if convert_all == 'true':
                selected_tables = MYSQL_TABLES

            do_embed = (embed == 'true')
            start_time = datetime.now()

            try:
                if selected_tables:
                    num_inserted_rows = convert_to_mongodb(selected_tables, do_embed)
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()

                    success_message = f"Conversion of {num_inserted_rows} items completed!"
                    insert_message_to_mysql(success_message, duration)
                    logger.info(success_message)

                    return render_template('convert.html', success_message=success_message)
                return render_template('convert.html', success_message="No tables selected.")
            except Exception as exc:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                error_message = f"Error during conversion: {str(exc)}"
                insert_message_to_mysql(error_message, duration)
                logger.error(error_message)

                return render_template('convert.html', success_message=error_message)

        return render_template('convert.html')

    @app.route('/update/<table_name>', methods=['POST'])
    def update_row(table_name):
        try:
            db = get_db(table_name)
        except Exception as e:
            flash(f"Database error: {e}", "danger")
            logger.error(f"Database error in update route: {e}")
            return redirect(url_for('view_table', selected_table=table_name))

        row_id = request.form.get('id')
        update_data = {k: v for k, v in request.form.items() if k != 'id'}

        try:
            if table_name in ALLOWED_TABLES:
                cursor = db.cursor()
                set_clause = ", ".join(f"{key} = %s" for key in update_data.keys())
                query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"

                values = list(update_data.values()) + [row_id]
                cursor.execute(query, values)
                db.commit()
                cursor.close()
            else:
                db.update_one({"id": int(row_id)}, {"$set": update_data})

            flash(f"Row updated successfully in {table_name}", "success")
            logger.info(f"Row updated in {table_name}, ID={row_id}")
        except Exception as e:
            flash(f"Error updating row: {str(e)}", "danger")
            logger.error(f"Update error in {table_name}: {e}")

        return redirect(url_for('view_table', selected_table=table_name))
