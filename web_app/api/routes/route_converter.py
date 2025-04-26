from datetime import datetime
from flask import render_template, request
from infrastructure.database.helpers.helpers import (
    convert_to_mongodb,
    insert_message_to_mysql,
    log_conversion_to_mysql  # <-- Neu importieren
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

        try:
            if selected_tables:
                start_time = datetime.now()

                for table_name in selected_tables:
                    num_inserted_rows = convert_to_mongodb([table_name], do_embed)

                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()

                    log_conversion_to_mysql(
                        source_table=table_name,
                        target_collection=f"{table_name}_embedded" if do_embed else f"{table_name}_flat",
                        status="success",
                        duration=duration
                    )

                success_message = f"Conversion of {len(selected_tables)} table(s) completed!"
                logger.info(success_message)
                return render_template('convert.html', success_message=success_message)

            return render_template('convert.html', success_message="No tables selected.")

        except Exception as exc:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            error_message = f"Error during conversion: {str(exc)}"
            logger.error(error_message)

            log_conversion_to_mysql(
                source_table="multiple",
                target_collection="mongodb",
                status="error",
                duration=duration
            )

            return render_template('convert.html', success_message=error_message)

    return render_template('convert.html')