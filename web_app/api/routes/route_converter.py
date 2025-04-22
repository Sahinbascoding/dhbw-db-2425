# Datei: api/routes/route_convert.py

from datetime import datetime
from flask import render_template, request
from infrastructure.database.helpers.helpers import (
    convert_to_mongodb, insert_message_to_mysql
)
from infrastructure.config.config import MYSQL_TABLES
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
