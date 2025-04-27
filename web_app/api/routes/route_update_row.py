# Datei: api/routes/route_update_row.py

from flask import request, redirect, url_for, flash
from infrastructure.database.helpers.helpers import get_db
from infrastructure.config.config import ALLOWED_TABLES
import logging

logger = logging.getLogger(__name__)

# Mapping Tabelle
PRIMARY_KEYS = {
    'fahrzeug': ['fahrzeugid'],
    'fahrer': ['fahrerid'],
    'fahrer_fahrzeug': ['fahrerid', 'fahrzeugid'],
    'fahrt': ['fahrtid'],
    'fahrt_fahrer': ['fahrtid', 'fahrerid'],
    'geraet': ['geraetid'],
    'fahrzeugparameter': ['fahrzeugparameterid'],
    'beschleunigung': ['beschleunigungid'],
    'diagnose': ['diagnoseid'],
    'wartung': ['wartungid'],
    'geraet_installation': ['geraet_installationid'],
    'conversion_log': ['id'],
    'changelog': ['id']
}

def update_row(table_name):
    try:
        db = get_db(table_name)
    except Exception as e:
        flash(f"Database error: {e}", "danger")
        logger.error(f"Database error in update route: {e}")
        return redirect(url_for('view_table', selected_table=table_name))

    primary_keys = PRIMARY_KEYS.get(table_name, [])
    if not primary_keys:
        flash(f"No primary key mapping found for {table_name}", "danger")
        return redirect(url_for('view_table', selected_table=table_name))

    # Update-Daten aufbauen
    update_data = {k: v for k, v in request.form.items() if not k.startswith('primary_keys[')}

    # Primärschlüssel-Daten aufbauen
    pk_conditions = []
    pk_values = []
    for pk in primary_keys:
        pk_value = request.form.get(f'primary_keys[{pk}]')
        if pk_value is None:
            flash(f"Primary key {pk} missing for update.", "danger")
            return redirect(url_for('view_table', selected_table=table_name))
        pk_conditions.append(f"{pk} = %s")
        pk_values.append(pk_value)

    try:
        if table_name in ALLOWED_TABLES:
            cursor = db.cursor()
            set_clause = ", ".join(f"{key} = %s" for key in update_data.keys())
            where_clause = " AND ".join(pk_conditions)
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            values = list(update_data.values()) + pk_values
            cursor.execute(query, values)
            db.commit()
            cursor.close()

        flash(f"Row updated successfully in {table_name}", "success")
        logger.info(f"Row updated in {table_name}, PKs={pk_values}")
    except Exception as e:
        flash(f"Error updating row: {str(e)}", "danger")
        logger.error(f"Update error in {table_name}: {e}")

    return redirect(url_for('view_table', selected_table=table_name))
