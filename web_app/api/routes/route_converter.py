# Datei: web_app/api/routes/route_converter.py

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from infrastructure.database.helpers.helpers import (
    convert_to_mongodb,
    insert_message_to_mysql,
    log_conversion_to_mysql
)
from infrastructure.config.config import MYSQL_TABLES, ALLOWED_TABLES
import logging

logger = logging.getLogger(__name__)

def convert():
    if request.method == 'POST':
        selected_tables = request.form.getlist('tables')
        convert_all = request.form.get('convert_all')
        embed = request.form.get('embed')

        if convert_all == 'true':
            selected_tables = MYSQL_TABLES

        do_embed = (embed == 'true')

        try:
            if selected_tables:
                logger.info(f"Selected tables for conversion: {selected_tables}")
                start_time = datetime.now()

                num_inserted_rows = convert_to_mongodb(selected_tables, do_embed)

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                successful_conversions = 0  # Zähler neu

                for table_name in selected_tables:
                    try:
                        log_conversion_to_mysql(
                            source_table=table_name,
                            target_collection=f"{table_name}_embedded" if do_embed else f"{table_name}_flat",
                            status="success",
                            duration=duration
                        )
                        logger.info(f"Logged conversion for table: {table_name}")
                        successful_conversions += 1
                    except Exception as log_exc:
                        logger.error(f"Error logging conversion for table {table_name}: {log_exc}")

                # WICHTIG: Nur eine Flash-Message abhängig von do_embed
                if do_embed:
                    flash(f"✅ Erfolgreich {num_inserted_rows} Dokumente eingebettet!", "success")
                else:
                    flash(f"✅ Erfolgreich {successful_conversions} Tabellen/Collections konvertiert!", "success")

                return redirect(url_for('index'))


            flash("⚠️ Keine Tabellen ausgewählt.", "warning")
            return redirect(url_for('convert'))

        except Exception as exc:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.error(f"Fehler bei der Konvertierung: {exc}", exc_info=True)

            log_conversion_to_mysql(
                source_table="multiple",
                target_collection="mongodb",
                status="error",
                duration=duration
            )

            flash("❌ Fehler bei der Konvertierung! Bitte Logs prüfen.", "danger")
            return redirect(url_for('convert'))

    return render_template('convert.html')
