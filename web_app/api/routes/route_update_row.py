# Datei: api/routes/route_update_row.py

from flask import request, redirect, url_for, flash
from infrastructure.database.helpers.helpers import get_db
from infrastructure.config.config import ALLOWED_TABLES
import logging

logger = logging.getLogger(__name__)

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
